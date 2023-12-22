from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def login_page():
        title = "Авторизация"
        return render_template("login.html", page_title=title)

    @app.route("/dashboard.html")
    def base():
        title = "Доски"
        return render_template("dashboard.html", page_title=title)

    @app.route("/tasks.html")
    def task():
        title = "Задачи"
        return render_template("tasks.html", page_title=title)

    return app