import os
import time

from celery import Celery

celery = Celery(__name__)

celery.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://host.docker.internal:6379/3')
celery.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://host.docker.internal:6379/3')

@celery.task(name='parse_tg')
def parse_tg(task_type):
    pass