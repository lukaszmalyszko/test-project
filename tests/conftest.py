import os

import pytest

from project import create_app, db, download_contents_blueprint
from settings import LOCAL_ENV


@pytest.fixture
def test_client():
    os.environ["RUN_MODE"] = LOCAL_ENV
    flask_app = create_app()
    flask_app.debug = True
    flask_app.testing = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    flask_app.config["SECRET_KEY"] = "bad_secret_key"
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def init_database(test_client):
    db.create_all()

    yield

    db.drop_all()


@pytest.fixture
def blueprint():
    return download_contents_blueprint
