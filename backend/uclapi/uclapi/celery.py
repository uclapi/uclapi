from __future__ import absolute_import, unicode_literals

import celery
import os
import raven

from django.conf import settings
from raven.contrib.celery import register_signal as raven_register_signal, \
    register_logger_signal as raven_register_logger_signal

from dotenv import read_dotenv


read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uclapi.settings')


class Celery(celery.Celery):
    def on_configure(self):
        if os.environ.get("SENTRY_DSN") != "":
            client = raven.Client(os.environ.get("SENTRY_DSN"))
            raven_register_logger_signal(client)
            raven_register_signal(client)


app = Celery('uclapi')

app.config_from_object('django.conf.settings', namespace='CELERY')


from opbeat.contrib.django.models import \
    register_handlers as opbeat_register_handlers, \
    logger as opbeat_logger  # noqa: E402#

from opbeat.contrib.celery import \
    register_signal as opbeat_register_signal  # noqa: E402


try:
    opbeat_register_signal(app)
except Exception as e:
    opbeat_logger.exception('Failed installing celery hook: %s' % e)

if 'opbeat.contrib.django' in settings.INSTALLED_APPS:
    opbeat_register_handlers()

app.autodiscover_tasks()


@app.task(bind=True)
def task(self):
    print('Request: {0!r}'.format(self.request))
