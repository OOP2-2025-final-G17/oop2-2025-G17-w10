from flask import Flask, render_template, request, session
from datetime import date
import json
from services.report import (
    monthly_summary,
    user_monthly_summary,
    user_ytd_summary,
    all_users_monthly_salary,
    all_users_ytd_salary,
)
from models import initialize_database, User
from routes import blueprints

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
    all_monthly_salaries = all_users_monthly_salary(year, month)
    all_ytd_salaries = all_users_ytd_salary(year, month)

    # JSONとしてテンプレートに渡す
    monthly_salary_json = json.dumps([s["salary"] for s in all_monthly_salaries])
    ytd_salary_json = json.dumps([s["salary"] for s in all_ytd_salaries])
    user_names_json = json.dumps([s["user_name"] for s in all_monthly_salaries])

    return render_template(
        "index.html",
        title="シフト管理システム",
        year=year,
        month=month,
        users=users,
        user_id=user_id,
        monthly_row=monthly_row,
        ytd_row=ytd_row,
        year_options=year_options,
        month_options=month_options,
        monthly_salary_json=monthly_salary_json,
        ytd_salary_json=ytd_salary_json,
        user_names_json=user_names_json,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
