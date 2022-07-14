from __future__ import absolute_import

from celery import Celery
from celery.signals import worker_process_shutdown, worker_process_init
from django.conf import settings

from configuration.utils import set_running_environment

set_running_environment()

app = Celery("products_management")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@worker_process_init.connect
def init_worker(**kwargs):
    print("Worker initialized.")


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    print("Worker shut down.")
