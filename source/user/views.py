from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from source.user.forms import LoginForm, RegistrationForm
from source.lib.db import User_DB
from source.lib.config import SQLALCHEMY_DATABASE_URI

blueprint = Blueprint("user", __name__, url_prefix="/user")
data_base = User_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('board.get_all_boards'))
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
        user = data_base.validate_user(form.login.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('board.get_all_boards'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.login'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template(
        'user/registration.html',
        page_title=title,
        form=form
    )


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        data_base.add_user(
            login=form.login.data,
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            patronymic=form.patronymic.data,
            position=form.position.data,
            role='user'
        )
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text,
                        error
                    )
                )
        flash('Пожалуйста, исправьте ошибки в форме')
        return redirect(url_for('user.register'))
