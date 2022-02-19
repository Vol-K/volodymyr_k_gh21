import sys
from os import (path, environ)

import django
from celery import Celery

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


celery_app = Celery("app", brocker="pyamqp://guest@localhost/")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
