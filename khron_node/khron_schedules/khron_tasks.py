from os import environ
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

def make_celery(app):
    celery = Celery(app, broker=environ['CELERY_BROKER_URL'])
    return celery

Khron_tasks = make_celery('khron_tasks')