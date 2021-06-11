from os import environ
from celery import Celery 
from celery.schedules import crontab
from web3 import Web3
import json
from dotenv import load_dotenv


app = Celery('khron_node',
             broker='localhost',
             include=['khron_node.khron_tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()