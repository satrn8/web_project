from flask import render_template, Blueprint

blueprint = Blueprint("user", __name__, url_prefix="/login")

@blueprint.route("/")
def login_page():
    title = "Авторизация"
    return render_template("login.html", page_title=title)