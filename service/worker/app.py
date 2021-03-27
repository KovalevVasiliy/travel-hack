from celery import Celery

from conf import REDIS_URL, celery_settings

app = Celery(
    'worker',
    broker=f'{REDIS_URL}/{celery_settings.TASKS_DB}',
    result_backend=f'{REDIS_URL}/{celery_settings.RESULT_DB}',
)
app.conf.broker_transport_options = {'visibility_timeout': 60 * 15}  # 15 minutes

from .tasks import *  # isort:skip
