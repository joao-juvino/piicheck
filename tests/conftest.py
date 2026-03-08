import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from run import create_app
from app.extensions import db
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():

    app = create_app("test")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(app):

    with app.app_context():
        token = create_access_token(identity="1")

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def mock_celery(mocker):
    return mocker.patch("app.modules.pii.pii_tasks.process_scan.delay")

