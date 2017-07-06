from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from dotenv import read_dotenv


read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uclapi.settings')

app = Celery('uclapi')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf.settings', namespace='CELERY')

# app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task(bind=True)
def task(self):
    print('Request: {0!r}'.format(self.request))
