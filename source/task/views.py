from flask import render_template, Blueprint

blueprint = Blueprint("task", __name__, url_prefix="/users")


@blueprint.route("/tasks")
def get_task():
    user_tasks = [
        {"number_task": 34, "title": "Создание приложения", "author": "Максим", "performer": "Иван",
         "description": "Однозначно, сделанные на базе интернет-аналитики выводы, вне зависимости от их уровня, должны быть рассмотрены исключительно в разрезе маркетинговых и финансовых предпосылок!",
         "status": "Закрыта", "starttime": "01.01.2023", "endtime": "03.01.2023"},
        {"number_task": 6, "title": "Написание API", "author": "Ольга", "performer": "Иван",
         "description": "Имеется спорная точка зрения, гласящая примерно следующее: диаграммы связей и по сей день остаются уделом либералов, которые жаждут быть своевременно верифицированы.",
         "status": "В работе", "starttime": "01.01.2023", "endtime": False},
        {"number_task": 77, "title": "Добавление полей", "author": "Максим", "performer": "Иван",
         "description": "Однозначно, сделанные на базе интернет-аналитики выводы, вне зависимости от их уровня, должны быть рассмотрены исключительно в разрезе маркетинговых и финансовых предпосылок!",
         "status": "Открыта", "starttime": "01.01.2023", "endtime": False},
        {"number_task": 56, "title": "Правка багов", "author": "Ольга", "performer": "Иван",
         "description": "Имеется спорная точка зрения, гласящая примерно следующее: диаграммы связей и по сей день остаются уделом либералов, которые жаждут быть своевременно верифицированы.",
         "status": "Открыта", "starttime": "01.01.2023", "endtime": False}
    ]
    title = "Задачи"
    return render_template("tasks.html", page_title=title, user_tasks=user_tasks)
