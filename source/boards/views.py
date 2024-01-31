from flask import render_template, Blueprint
from lib.db import Board_DB
from lib.config import connection_url

blueprint = Blueprint("board", __name__, url_prefix="/boards")
data_base = Board_DB(connection_url)


@blueprint.route("/")
def get_all_boards():
    all_boards = data_base.get_boards()
    title = "Доски"
    return render_template(
        "boards.html",
        page_title=title,
        all_boards=all_boards
    )
