# Import all necessary moduls:
# 1) Import "system" packages.
import sys
from os import (path, environ)

# 2) from Django package.
import django

# 3) from Celery package.
from celery import Celery
from celery.schedules import crontab


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery("app", brocker="pyamqp://guest@localhost/")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Scheduled periodic tasks.
app.conf.beat_schedule = {
    'daily-check-for-match_datetime': {
        'task': 'admin_side.tasks.task_every_day_check_match_score',
        'schedule': crontab(minute='*/3'),
        # 'schedule': crontab(hour=1, minute=15),
    },
    "hourly-check-if-user-made-forecast": {
        "task": "admin_side.tasks.task_every_hour_done_forecasts_check",
        'schedule': crontab(minute='*/3'),
        # "schedule": crontab(hour="*", minute=10),
    },
}
app.autodiscover_tasks()
