from flask import render_template, Blueprint
from flask_login import login_required
from lib.db import Task_DB
from lib.config import SQLALCHEMY_DATABASE_URI


blueprint = Blueprint("task", __name__, url_prefix="/tasks")
data_base = Task_DB(SQLALCHEMY_DATABASE_URI)

@blueprint.route("/")
@login_required
def get_task():
    user_tasks = data_base.get_tasks()
    title = "Задачи"
    return render_template(
        "task/tasks.html",
        page_title=title,
        user_tasks=user_tasks
    )
