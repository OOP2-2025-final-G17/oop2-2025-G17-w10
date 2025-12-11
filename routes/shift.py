from flask import Blueprint, render_template, request, redirect, url_for
from models import shift
from datetime import datetime

# Blueprintの作成
shift_bp = Blueprint("shift", __name__, url_prefix="/shifts")


@shift_bp.route("/")
def list():
    shifts = shift.Shift.select()
    return render_template("shift_list.html", title="シフト一覧", items=shifts)


@shift_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        workplace = request.form["workplace"]
        date = request.form["date"]
        shift.Shift.create(name=name, workplace=workplace, date=date)
        return redirect(url_for("shift.list"))
    return render_template("shift_add.html")


@shift_bp.route("/edit/<int:shift_id>", methods=["GET", "POST"])
def edit(shift_id):
    shift_instance = shift.Shift.get_or_none(shift.Shift.id == shift_id)
    if not shift_instance:
        return redirect(url_for("shift.list"))
    if request.method == "POST":
        shift_instance.name = request.form["name"]
        shift_instance.workplace = request.form["workplace"]
        shift_instance.date = request.form["date"]
        shift_instance.save()
        return redirect(url_for("shift.list"))
    return render_template("shift_edit.html", shift=shift_instance)
