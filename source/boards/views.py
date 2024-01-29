from flask import render_template, Blueprint
from lib.db import Board_DB
from lib.config import SQLALCHEMY_DATABASE_URI
from flask_login import login_required

blueprint = Blueprint("board", __name__, url_prefix="/boards")
data_base = Board_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/")
@login_required
def get_all_boards():
    all_boards = data_base.get_boards()
    title = "Доски"
    return render_template(
        "boards.html",
        page_title=title,
        all_boards=all_boards
    )
