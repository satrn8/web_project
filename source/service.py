from flask import Flask, render_template
from source.user.views import blueprint as user_blueprint


class Service:
    def __init__(self, host=None, port=None, debug=None):
        self.app = Flask(__name__)

    def add_routes(self):
        self.app.register_blueprint(user_blueprint)

    def start(self):
        self.add_routes()
        self.app.run()


if __name__ == '__main__':
    service = Service()
    service.start()