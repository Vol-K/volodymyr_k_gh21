import sys
from os import (path, environ)

import django
from celery import Celery
from celery.schedules import crontab


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
# django.setup()

app = Celery("app", brocker="pyamqp://guest@localhost/")
app.config_from_object("django.conf:settings", namespace="CELERY")

#
app.conf.beat_schedule = {
    # Executes every minutes
    # 'daily-check-for-match_datetime': {
    #     'task': 'admin_side.tasks.task_every_minute_printing',
    #     'schedule': crontab(minute='*/1'),
    #     # 'schedule': crontab(minute=53, hour=0),
    # },
    "daily-check-if-user-made-forecast": {
        "task": "admin_side.tasks.task_every_hour_done_forecasts_check",
        "schedule": crontab(minute="*/1"),
    },
}
app.autodiscover_tasks()
