from flask import Flask

from signet.models import db
from signet.oauth2_server import config_oauth
from signet.routes import bp


def create_app(config):
    app = Flask(__name__)

    # load app specified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    setup_app(app)
    return app


def setup_app(app):
    db.init_app(app)

    # Create tables if they do not exist already
    with app.app_context():
        db.create_all()

    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')
