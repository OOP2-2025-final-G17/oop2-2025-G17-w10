from flask import Flask, render_template, request, session
from datetime import date
import json
from static.scripts.report import (
    monthly_summary,
    user_monthly_summary,
    user_ytd_summary,
    all_users_monthly_salary,
    all_users_ytd_salary,
)
from models import initialize_database, User
from routes import blueprints
from models.db import db
from models.user import User
from models.workplace import Workplace
from models.time import Time
from models.shift import Shift
from collections import OrderedDict
import json

app = Flask(__name__)
app.secret_key = "shift-management-secret"  # セッション用の秘密鍵

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)


# ホームページのルート
@app.route("/", methods=["GET", "POST"])
def index():
    today_date = date.today()            
    today = date.today()

    # POSTリクエスト時にセッションに値を保存
    if request.method == "POST":
        year = int(request.form.get("year", today.year))
        month = int(request.form.get("month", today.month))
        user_id = request.form.get("user_id", None)

        session["report_year"] = year
        session["report_month"] = month
        session["report_user_id"] = user_id

    # セッションから値を取得（POSTなければデフォルト）
    year = session.get("report_year", today.year)
    month = session.get("report_month", today.month)
    user_id = session.get("report_user_id", None)

    # ユーザー一覧
    users = User.select()

    # 月次集計または年初からの集計を取得
    monthly_row = None
    ytd_row = None
    if user_id:
        user_id_int = int(user_id) if isinstance(user_id, str) else user_id
        monthly_row = user_monthly_summary(user_id_int, year, month)
        ytd_row = user_ytd_summary(user_id_int, year, month)

    # 年と月のオプション
    year_options = list(range(today.year - 2, today.year + 3))
    month_options = list(range(1, 13))

    # 全ユーザーの月次・年初来給与データ（グラフ用）
    all_users_monthly_rows = monthly_summary(year, month)
    all_monthly_salaries = all_users_monthly_salary(year, month)
    all_ytd_salaries = all_users_ytd_salary(year, month)

    # JSONとしてテンプレートに渡す
    monthly_salary_json = json.dumps([s["salary"] for s in all_monthly_salaries])
    ytd_salary_json = json.dumps([s["salary"] for s in all_ytd_salaries])
    user_names_json = json.dumps([s["user_name"] for s in all_monthly_salaries])

    query = (
        Shift.select(Shift, Workplace, User)
        .join(Workplace)  # Shift.workplace
        .switch(Shift)
        .join(User)  # Shift.user
        .order_by(Workplace.name, User.name)
    )
    workplace_to_users = OrderedDict()

    for s in query:
        wp_name = s.workplace.name
        if wp_name not in workplace_to_users:
            workplace_to_users[wp_name] = OrderedDict()

        # 同じ職場に同じ人が複数シフトあっても 1 回だけ表示
        workplace_to_users[wp_name][s.user.id] = s.user.name
    groups = [
        {"workplace": wp_name, "users": list(users.values())}
        for wp_name, users in workplace_to_users.items()
    ]
    chart_labels = list(workplace_to_users.keys())
    chart_data = [len(uids) for uids in workplace_to_users.values()]

    shifts = Shift.select().where(Shift.date == today_date).join(Workplace).switch(Shift).join(User).order_by(Workplace.name, User.name,Shift.date)

    return render_template(
        "index.html",
        title="シフト管理システム",
        year=year,
        month=month,
        users=users,
        user_id=user_id,
        monthly_row=monthly_row,
        ytd_row=ytd_row,
        all_users_monthly_rows=all_users_monthly_rows,
        year_options=year_options,
        month_options=month_options,
        monthly_salary_json=monthly_salary_json,
        ytd_salary_json=ytd_salary_json,
        user_names_json=user_names_json,
        groups=groups,
        chart_labels=json.dumps(chart_labels, ensure_ascii=False),
        chart_data=json.dumps(chart_data),
        today=today_date,
        today_shifts=shifts,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
