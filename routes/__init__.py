from flask import Blueprint, render_template
from .user import user_bp
from .workplace import workplace_bp
from .shift import shift_bp
from .time import time_bp
from .calendar import calendar_bp
from models.shift import Shift
from models.user import User
from models.workplace import Workplace

# Blueprint をまとめる
blueprints = [user_bp, workplace_bp, time_bp, shift_bp, calendar_bp]

# トップページ用 Blueprint
bp = Blueprint("index", __name__)

@bp.route("/")
def index():
    # Peewee でシフトデータを取得（user, workplace を join）
    shift_items = (
        Shift.select(Shift, User, Workplace)
             .join(User)
             .switch(Shift)
             .join(Workplace)
    )

    # FullCalendar 用の JSON に変換
    shifts = []
    for shift in shift_items:
        # ユーザー名と職場名を title に表示
        shifts.append({
            "title": f"{shift.user.name} ({shift.workplace.name})",
            "start": str(shift.date),  # YYYY-MM-DD
            "end": str(shift.date)     # 同日終日
        })

    return render_template("index.html", shifts=shifts)