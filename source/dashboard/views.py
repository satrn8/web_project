from flask import render_template, Blueprint, redirect, request
from lib.db import Task_DB
from lib.config import SQLALCHEMY_DATABASE_URI
from flask_login import login_required

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")
data_base = Task_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/<int:board_id>", methods=["GET"])
@login_required
def get_dashboard(board_id):
    dashboard = data_base.get_tasks(board_id)
    title = "Доска"
    return render_template("dashboard.html", page_title=title, dashboard=dashboard, board_id=board_id)


@blueprint.route("/change_status", methods=["GET"])
@login_required
def change_status():
    task_id = request.args.get("task_id")
    status = request.args.get("task_status")
    board_id = request.args.get("board_id")
    print(task_id, status)
    data_base.change_status(task_id, status)
    return redirect(f"/dashboard/{board_id}")
