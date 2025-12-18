from flask import Blueprint, render_template, request, redirect, url_for
from models import workplace

# Blueprintの作成
workplace_bp = Blueprint("workplace", __name__, url_prefix="/workplaces")


@workplace_bp.route("/")
def list():
    workplaces = workplace.select()
    return render_template("workplace_list.html", title="職場", items=workplaces)


@workplace_bp.route("/add", methods=["GET", "POST"])
def add():

    # POSTで送られてきたデータは登録
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        workplace.create(name=name, price=price)
        return redirect(url_for("workplace.list"))

    return render_template("workplace_add.html")


@workplace_bp.route("/edit/<int:workplace_id>", methods=["GET", "POST"])
def edit(workplace_id):
    workplace_item = workplace.get_or_none(workplace.id == workplace_id)
    if not workplace_item:
        return redirect(url_for("workplace.list"))

    if request.method == "POST":
        workplace_item.name = request.form["name"]
        workplace_item.price = request.form["price"]
        workplace_item.save()
        return redirect(url_for("workplace.list"))

    return render_template("workplace_edit.html", workplace=workplace_item)
