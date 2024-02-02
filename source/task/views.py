from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from lib.db import Task_DB
from lib.config import SQLALCHEMY_DATABASE_URI
from task.forms import NewTaskForm
from datetime import datetime

blueprint = Blueprint("task", __name__, url_prefix="/tasks")
data_base = Task_DB(SQLALCHEMY_DATABASE_URI)


@blueprint.route("/")
@login_required
def get_my_task():
    user_tasks = data_base.get_my_tasks()
    title = "Задачи"
    return render_template(
        "task/tasks.html",
        page_title=title,
        user_tasks=user_tasks
    )


@blueprint.route("/new/<int:board_id>")
@login_required
def new_task(board_id):
    form = NewTaskForm()
    title = "Новая задача"
    return render_template(
        "task/create_task.html",
        page_title=title,
        board_id=board_id,
        form=form
    )


@blueprint.route('/create-task', methods=['POST'])
def process_create_task():
    form = NewTaskForm()
    board_id = request.args.get("board_id")
    print(board_id)
    if form.validate_on_submit():
        data_base.add_task(
            board_id=board_id,
            title=form.title.data,
            description=form.description.data,
            author=current_user.id,
            assigned_to=current_user.id,
            published=datetime.now(),
            finish_date=datetime.now(),
            planned_finish_date=datetime.now(),
            planned_spent_time=0,
            spent_time=0,
            status='Открыта'
        )
        return redirect(f"/dashboard/{board_id}")
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
        return redirect(url_for('task.create_task', board_id=board_id))
