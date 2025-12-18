from flask import Blueprint, render_template, request, redirect, url_for
from models import Shift, Time, User, Workplace
from datetime import datetime

# Blueprintの作成
shift_bp = Blueprint("shift", __name__, url_prefix="/shifts")


@shift_bp.route("/")
def list():
    shifts = Shift.select()
    return render_template("shift_list.html", title="シフト一覧", items=shifts)


@shift_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        user_id = request.form["user_id"]
        workplace_id = request.form["workplace_id"]
        date = request.form["date"]
        time_id = request.form["time_id"]
        Shift.create(user=user_id, workplace=workplace_id, date=date, time=time_id)
        return redirect(url_for("shift.list"))
    users = User.select()
    workplaces = Workplace.select()
    times = Time.select()
    return render_template(
        "shift_add.html", users=users, workplaces=workplaces, times=times
    )


@shift_bp.route("/edit/<int:shift_id>", methods=["GET", "POST"])
def edit(shift_id):
    shift_instance = Shift.get_or_none(Shift.id == shift_id)
    if not shift_instance:
        return redirect(url_for("shift.list"))
    if request.method == "POST":
        shift_instance.user = request.form["user_id"]
        shift_instance.workplace = request.form["workplace_id"]
        shift_instance.date = request.form["date"]
        shift_instance.time = request.form["time_id"]
        shift_instance.save()
        return redirect(url_for("shift.list"))
    users = User.select()
    workplaces = Workplace.select()
    times = Time.select()
    return render_template(
        "shift_edit.html",
        shift=shift_instance,
        users=users,
        workplaces=workplaces,
        times=times,
    )
