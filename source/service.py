from flask import Flask, render_template
from source.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint)

    @app.route("/")
    def login_page():
        title = "Авторизация"
        return render_template("login.html", page_title=title)

    return app