from flask import render_template, Blueprint, redirect, request
from lib.db import Task_DB
from lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")
data_base = Task_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/", methods=["GET"])
def get_dashboard():
    dashboard = data_base.get_task()
    title = "Доска"
    return render_template("dashboard.html", title=title, dashboard=dashboard)


@blueprint.route("/change_status", methods=["GET"])
def change_status():
    task_id = request.args.get("task_id")
    status = request.args.get("task_status")
    print(task_id, status)

    data_base.change_status(task_id, status)

    return redirect("/dashboard")
