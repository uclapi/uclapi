from __future__ import absolute_import

import json

import redis

from celery import shared_task
from django.conf import settings


@shared_task
def cache_student_timetable(upi, timetable_data):
    timetable_key = "timetable:personal:{}".format(upi)

    r = redis.Redis(
        host=settings.REDIS_UCLAPI_HOST,
        charset="utf-8",
        decode_responses=True
    )

    r.set(
        timetable_key,
        json.dumps(timetable_data),
        ex=43200
    )
