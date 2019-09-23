from __future__ import absolute_import, unicode_literals

import celery
import os
import raven

from raven.contrib.celery import register_signal as raven_register_signal, \
    register_logger_signal as raven_register_logger_signal

from common.helpers import read_dotenv

read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uclapi.settings')


class Celery(celery.Celery):
    def on_configure(self):
        if os.environ.get("SENTRY_DSN") is not None:
            client = raven.Client(os.environ.get("SENTRY_DSN"))
            raven_register_logger_signal(client)
            raven_register_signal(client)


app = Celery('uclapi')

app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def task(self):
    print('Request: {0!r}'.format(self.request))
