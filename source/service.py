from flask import Flask
from source.user.task import blueprint as task_blueprint
from source.user.dashboard import blueprint as dashboard_blueprint


class Service:
    def __init__(self, host=None, port=None, debug=None):
        self.app = Flask(__name__)

    def add_routes(self):
        self.app.register_blueprint(dashboard_blueprint)
        self.app.register_blueprint(task_blueprint)

    def start(self):
        self.add_routes()
        self.app.run()


if __name__ == '__main__':
    service = Service()
    service.start()