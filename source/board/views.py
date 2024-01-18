from flask import render_template, Blueprint
from source.lib.db import DB
from source.lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("board", __name__, url_prefix="/boards")
data_base = DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/")
def get_boards():
    all_boards = data_base.get_boards()
    print(all_boards)
    title = "Доски"
    return render_template(
        "board.html",
        page_title=title,
        all_boards=all_boards
    )
