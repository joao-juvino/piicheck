from flask import Flask

from app.config.config import Config
from app.extensions.celery_app import init_celery
from app.extensions.extensions import db, jwt, limiter, migrate
from app.modules.auth.auth_routes import auth_bp
from app.modules.pii.pii_routes import pii_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    init_celery(app)

    # extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pii_bp, url_prefix="/pii")

    return app