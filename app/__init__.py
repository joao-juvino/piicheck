from flask import Flask
from flask_smorest import Api

from app.config.config import Config
from app.extensions.celery_app import init_celery
from app.extensions.extensions import db, jwt, limiter, migrate


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == "test":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["JWT_SECRET_KEY"] = "a_very_long_secret_key_for_testing_purposes"

    app.config.from_object(Config)

    init_celery(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    api = Api(app)

    from app.modules.auth.auth_routes import auth_blp
    from app.modules.pii.pii_routes import pii_blp

    api.register_blueprint(auth_blp)
    api.register_blueprint(pii_blp)

    return app