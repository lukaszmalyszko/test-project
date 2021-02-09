import logging

from app import app as flask_app
from project.worker import app as celery


def make_celery():
    celery.init_app(flask_app)
    logging.error(f"dupa{flask_app.config}")
    return celery


app = make_celery()
