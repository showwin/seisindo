from flask import Flask

from app.view import view


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.BaseConfig')

    app.register_blueprint(view)
    return app
