from flask import render_template, Blueprint
from lib.db import Board_DB
from lib.config import connection_url

blueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")
data_base = Board_DB(connection_url)


@blueprint.route("/<int:board_id>")
def get_dashboard(board_id):
    title = data_base.get_board(board_id)
    return render_template("dashboard.html", page_title=title)
