from flask import Blueprint, render_template
from models.shift import Shift
from models.user import User
from models.workplace import Workplace

index_bp = Blueprint("index", __name__)

@index_bp.route("/")
def index():
    shift_items = (
        Shift.select(Shift, User, Workplace)
             .join(User)
             .switch(Shift)
             .join(Workplace)
    )

    shifts = []
    for shift in shift_items:
        shifts.append({
            "title": f"{shift.user.name} ({shift.workplace.name})",
            "start": str(shift.date),
        })

    return render_template("index.html", shifts=shifts)