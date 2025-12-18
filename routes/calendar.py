from flask import Blueprint, render_template
from models.shift import Shift  # Shiftモデルをインポート

calendar_bp = Blueprint(
    "calendar",
    __name__,
    url_prefix="/calendar"
)

@calendar_bp.route("/")
def index():
    # 1. データベースからシフト情報を取得
    # .join を使って、関連する職場(Workplace)と時間(Time)の情報も一緒に持ってくるのがコツです
    shift_items = Shift.select()

    shifts = []
    for shift in shift_items:
        # FullCalendarが読み取れる形式（dict）に変換
        shifts.append({
            "title": f"{shift.workplace.name} {shift.time.start_time}-{shift.time.end_time}",
            "start": str(shift.date) # YYYY-MM-DD の形式にする
        })

    # 2. テンプレートに shifts を渡す
    return render_template("calendar.html", shifts=shifts)