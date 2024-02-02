from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from lib.db import User_DB
from lib.config import SQLALCHEMY_DATABASE_URI


data_base = User_DB(SQLALCHEMY_DATABASE_URI)


class LoginForm(FlaskForm):
    login = StringField(
        'Логин пользователя',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={"class": "form-check-input"}
    )
    submit = SubmitField(
        'Отправить',
        render_kw={"class": "btn btn-primary"}
    )


class RegistrationForm(FlaskForm):
    login = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"class": "form-control"}
        )
    first_name = StringField(
        'Имя',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    last_name = StringField(
        'Фамилия',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    patronymic = StringField(
        'Отчество',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    position = StringField(
        'Должность',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Отправить!',
        render_kw={"class": "btn btn-primary"}
    )

    # Функция для проверки, что логин свободен
    def validate_login(self, login):
        login_count = data_base.login_counter(login.data)
        if login_count > 0:
            raise ValidationError(
                'Пользователь с таким именем '
                'уже зарегистрирован'
            )

    # Функция для проверки, что email свободен
    def validate_email(self, email):
        email_count = data_base.email_counter(email.data)
        if email_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной '
                'почтой уже зарегистрирован'
            )
