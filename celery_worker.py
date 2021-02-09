from celery import Celery

from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


def make_celery():
    return Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
