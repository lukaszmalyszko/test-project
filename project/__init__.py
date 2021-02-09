import os

from flask import Flask

from project.download_content import download_contents_blueprint
from project.models import db
from project.worker import app as celery
from settings import (CELERY_BROKER_URL, CELERY_RESULT_BACKEND, LOCAL_ENV,
                      STORAGE_URI)


def create_app() -> Flask:
    app = Flask(__name__)
    initialize_config(app)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app: Flask):
    db.init_app(app)
    celery.init_app(app)


def initialize_config(app: Flask):
    app.config["BROKER_URL"] = CELERY_BROKER_URL
    app.config["RESULT_BACKEND"] = CELERY_RESULT_BACKEND
    app.config["SQLALCHEMY_DATABASE_URI"] = STORAGE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def register_blueprints(app: Flask):
    app.register_blueprint(download_contents_blueprint)
