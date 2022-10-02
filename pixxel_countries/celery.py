import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pixxel_countries.settings")

app = Celery("pixxel_countries")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
