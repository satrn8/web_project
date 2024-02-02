from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from lib.db import User_DB
from lib.config import SQLALCHEMY_DATABASE_URI


data_base = User_DB(SQLALCHEMY_DATABASE_URI)


class NewTaskForm(FlaskForm):
    title = StringField(
        'Название задачи',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    description = TextAreaField(
        'Описание задачи',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Создать',
        render_kw={"class": "btn btn-primary"}
    )
