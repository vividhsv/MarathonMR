from flask import Flask, render_template

from MarathonMR.config import ProdConfig
from MarathonMR.public import views as public_views


def create_app(config_name=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_name)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_blueprints(app):
    app.register_blueprint(public_views.blueprint)
    return None


def register_extensions(app):
    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("errorhandlers/{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
