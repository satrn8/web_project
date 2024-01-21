from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from source.user.forms import LoginForm, RegistrationForm
from source.lib.models import User
from source.lib.db import DB
from source.lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("user", __name__, url_prefix="/user")
data_base = DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('boards'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template(
        "user/login.html",
        page_title=title,
        form=login_form
    )


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = data_base.get_user(form.login.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('boards'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))
