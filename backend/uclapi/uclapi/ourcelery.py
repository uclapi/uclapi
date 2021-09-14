from __future__ import absolute_import, unicode_literals

import celery
import os

from common.helpers import read_dotenv
from django_celery_beat.models import CrontabSchedule, PeriodicTask

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


gencache_schedule, _ = CrontabSchedule.objects.get_or_create(minute='5,35', hour='*',
                                                             day_of_week='*', day_of_month='*', month_of_year='*')

gencache_periodic_task = PeriodicTask.objects.filter(task='timetable.tasks.update_gencache_celery').first()
if gencache_periodic_task is None:
    gencache_periodic_task = PeriodicTask(task='timetable.tasks.update_gencache_celery')
gencache_periodic_task.crontab = gencache_schedule
gencache_periodic_task.name = 'Update gencache'
gencache_periodic_task.save()


@app.task(bind=True)
def task(self):
    print('Request: {0!r}'.format(self.request))
