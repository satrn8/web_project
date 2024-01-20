from flask import render_template, Blueprint
from source.lib.db import DB
from source.lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")
data_base = DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/<int:board_id>")
def get_dashboard(board_id):
    title = data_base.get_board(board_id)
    return render_template("dashboard.html", page_title=title)
