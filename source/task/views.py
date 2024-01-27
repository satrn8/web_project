from flask import render_template, Blueprint
from lib.db import Task_DB
from lib.config import connection_url

blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
data_base = Task_DB(connection_url)


@blueprint.route("/tasks")
def get_task():
    task = data_base.get_task()
    title = "Задачи"
    return render_template("tasks.html", title=title, task=task)
