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
            from sentry_sdk.integrations.celery import CeleryIntegration

            sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"),
                            integrations=[DjangoIntegration(), CeleryIntegration()],
                            traces_sample_rate=0.01,
                            send_default_pii=True)


app = Celery('uclapi')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import CrontabSchedule, PeriodicTask

    # Gencache at every 5th and 35th minute
    gencache_schedule, _ = CrontabSchedule.objects.get_or_create(minute='5,35', hour='*',
                                                                 day_of_week='*', day_of_month='*',
                                                                 month_of_year='*')

    gencache_periodic_task = PeriodicTask.objects.filter(task='timetable.tasks.update_gencache_celery').first()
    if gencache_periodic_task is None:
        gencache_periodic_task = PeriodicTask(task='timetable.tasks.update_gencache_celery')
    gencache_periodic_task.crontab = gencache_schedule
    gencache_periodic_task.name = 'Update gencache'
    gencache_periodic_task.save()

    # Day cache for occupeye every 2 minutes
    day_cache_schedule, _ = CrontabSchedule.objects.get_or_create(minute='*/2', hour='*',
                                                                  day_of_week='*', day_of_month='*',
                                                                  month_of_year='*')
    occupeye_day_periodic_task = PeriodicTask.objects.filter(task='workspaces.tasks.day_cache').first()
    if occupeye_day_periodic_task is None:
        occupeye_day_periodic_task = PeriodicTask(task='workspaces.tasks.day_cache')
    occupeye_day_periodic_task.crontab = day_cache_schedule
    occupeye_day_periodic_task.name = 'Occupeye day cache'
    occupeye_day_periodic_task.save()

    # Night cache for occupeye at 2AM every day
    night_cache_schedule, _ = CrontabSchedule.objects.get_or_create(minute='0', hour='2',
                                                                    day_of_week='*', day_of_month='*',
                                                                    month_of_year='*')
    occupeye_night_periodic_task = PeriodicTask.objects.filter(task='workspaces.tasks.night_cache').first()
    if occupeye_night_periodic_task is None:
        occupeye_night_periodic_task = PeriodicTask(task='workspaces.tasks.night_cache')
    occupeye_night_periodic_task.crontab = night_cache_schedule
    occupeye_night_periodic_task.name = 'Occupeye night cache'
    occupeye_night_periodic_task.save()

    # Update LibCal token every 30 minutes
    libcal_token_schedule, _ = CrontabSchedule.objects.get_or_create(minute='*/30', hour='*',
                                                                     day_of_week='*', day_of_month='*',
                                                                     month_of_year='*')
    libcal_token_task = PeriodicTask.objects.filter(task='libcal.tasks.refresh_libcal_token').first()
    if libcal_token_task is None:
        libcal_token_task = PeriodicTask(task='libcal.tasks.refresh_libcal_token')
    libcal_token_task.crontab = libcal_token_schedule
    libcal_token_task.name = 'LibCal token refresh'
    libcal_token_task.save()


@app.task()
def ping_sample_task():
    return True
