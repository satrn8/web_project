from flask import Flask
from source.task.views import blueprint as task_blueprint
from source.dashboard.views import blueprint as dashboard_blueprint
from source.boards.views import blueprint as board_blueprint
from source.user.views import blueprint as user_blueprint
from flask_login import LoginManager
from source.lib.models import User


class Service:
    def __init__(self, host=None, port=None, debug=None):
        self.app = Flask(__name__)
        self.app.config.from_pyfile("lib\config.py")
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'user.login'

        @self.login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    def add_routes(self):
        self.app.register_blueprint(dashboard_blueprint)
        self.app.register_blueprint(task_blueprint)
        self.app.register_blueprint(board_blueprint)
        self.app.register_blueprint(user_blueprint)

    def start(self):
        self.add_routes()
        self.app.run(debug=True)


if __name__ == '__main__':
    service = Service()
    service.start()
