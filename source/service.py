from flask import Flask
from source.user.task import blueprint as task_blueprint
from source.dashboard.views import blueprint as dashboard_blueprint
from source.boards.views import blueprint as board_blueprint


class Service:
    def __init__(self, host=None, port=None, debug=None):
        self.app = Flask(__name__)

    def add_routes(self):
        self.app.register_blueprint(dashboard_blueprint)
        self.app.register_blueprint(task_blueprint)
        self.app.register_blueprint(board_blueprint)

    def start(self):
        self.add_routes()
        self.app.run(debug=True)


if __name__ == '__main__':
    service = Service()
    service.start()
