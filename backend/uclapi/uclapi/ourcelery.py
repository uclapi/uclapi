from __future__ import absolute_import, unicode_literals

import celery
import os


from common.helpers import read_dotenv

read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uclapi.settings')


class Celery(celery.Celery):
    def on_configure(self):
        if os.environ.get("SENTRY_DSN") is not None:
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration

            sentry_sdk.init(
                dsn=os.environ.get("SENTRY_DSN"),
                integrations=[DjangoIntegration()],
                traces_sample_rate=0.01,
                send_default_pii=True
            )


app = Celery('uclapi')

app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def task(self):
    print('Request: {0!r}'.format(self.request))
