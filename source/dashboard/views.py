from flask import render_template, Blueprint
from lib.db import Task_DB
from lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")
data_base = Task_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/")
def get_dashboard():
    dashboard = data_base.get_task()

    title = "Доска"
    return render_template("dashboard.html", title=title, dashboard=dashboard)
