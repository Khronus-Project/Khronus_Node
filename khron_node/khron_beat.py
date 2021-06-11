from .celery import app
from celery.schedules import crontab
from dotenv import load_dotenv
from os import environ

load_dotenv()
app.conf.beat_schedule = {
    #Executes every minute
    'Testing': {
            'task': 'khron_node.khron_tasks.monitor_request',
            'schedule': crontab(),
            'args': (environ['ADDRESS'], environ['ABI_PATH']),
        },
    }