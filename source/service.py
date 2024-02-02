from flask import Flask
from task.views import blueprint as task_blueprint
from dashboard.views import blueprint as dashboard_blueprint
from boards.views import blueprint as board_blueprint
from user.views import blueprint as user_blueprint
from flask_login import LoginManager
from lib.db import User_DB
from lib.config import SQLALCHEMY_DATABASE_URI


data_base = User_DB(SQLALCHEMY_DATABASE_URI)


class Service:
    def __init__(self, host=None, port=None, debug=None):
        self.app = Flask(__name__)
        self.app.config.from_pyfile("lib/config.py")
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'user.login'

        @self.login_manager.user_loader
        def load_user(user_id):
            user = data_base.get_user(user_id)
            return user

    def add_routes(self):
        self.app.register_blueprint(dashboard_blueprint)
        self.app.register_blueprint(task_blueprint)
        self.app.register_blueprint(board_blueprint)
        self.app.register_blueprint(user_blueprint)

    def start(self):
        self.add_routes()
        # Запускаем в локальной сети
        self.app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == '__main__':
    service = Service()
    service.start()
