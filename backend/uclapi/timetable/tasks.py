from __future__ import absolute_import

import json
import time
from datetime import datetime

import redis
from celery import shared_task, chord
from django.conf import settings
from django.db import connections
from django import db
import gc

from common.helpers import LOCAL_TIMEZONE
from timetable.models import (
    Classifications, ClassificationsA, ClassificationsB,
    Cminstances, CminstancesA, CminstancesB,
    Crsavailmodules, CrsavailmodulesA, CrsavailmodulesB,
    Crscompmodules, CrscompmodulesA, CrscompmodulesB,
    Course, CourseA, CourseB,
    Depts, DeptsA, DeptsB,
    Lecturer, LecturerA, LecturerB,
    Module, ModuleA, ModuleB,
    Modulegroups, ModulegroupsA, ModulegroupsB,
    Sites, SitesA, SitesB,
    Stuclasses, StuclassesA, StuclassesB,
    Stumodules, StumodulesA, StumodulesB,
    Students, StudentsA, StudentsB,
    Timetable, TimetableA, TimetableB,
    Weekmapnumeric, WeekmapnumericA, WeekmapnumericB,
    Weekmapstring, WeekmapstringA, WeekmapstringB,
    Weekstructure, WeekstructureA, WeekstructureB,
    Lock
)

from roombookings.models import (
    Room, RoomA, RoomB,
    Booking, BookingA, BookingB
)


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


tables = [
    (Booking, BookingA, BookingB, True, True, True),
    (Cminstances, CminstancesA, CminstancesB, True, False, False),
    (Course, CourseA, CourseB, True, False, False),
    (Classifications, ClassificationsA, ClassificationsB, True, False, False),
    (Crsavailmodules, CrsavailmodulesA, CrsavailmodulesB, True, False, True),
    (Crscompmodules, CrscompmodulesA, CrscompmodulesB, True, False, True),
    (Depts, DeptsA, DeptsB, False, False, False),
    (Lecturer, LecturerA, LecturerB, True, False, True),
    (Module, ModuleA, ModuleB, True, False, False),
    (Room, RoomA, RoomB, True, True, False),
    (Sites, SitesA, SitesB, True, False, False),
    (Stuclasses, StuclassesA, StuclassesB, True, False, False),
    (Stumodules, StumodulesA, StumodulesB, True, False, True),
    (Students, StudentsA, StudentsB, True, False, True),
    (Timetable, TimetableA, TimetableB, True, False, True),
    (Modulegroups, ModulegroupsA, ModulegroupsB, True, False, True),
    (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, True, False, False),
    (Weekmapstring, WeekmapstringA, WeekmapstringB, True, False, False),
    (Weekstructure, WeekstructureA, WeekstructureB, True, False, False),
]


@shared_task(queue="gencache")
def cache_table_task_testing(idx, dest_table_idx, load_batch_size=10000, insert_batch_size=5000):
    print(f"Inside cache_table_task_testing with index {idx}")
    time.sleep(20)
    return None


@shared_task(queue="gencache")
def completion_callback(_, running_key, start_time):
    redis_conn = redis.Redis(host=settings.REDIS_UCLAPI_HOST,
                             charset="utf-8",
                             decode_responses=True)
    elapsed_time = time.time() - start_time
    print(
        "Caching process completed in {}m {}s".format(
            int(elapsed_time // 60),
            int(elapsed_time % 60)
        )
    )

    print("Inverting lock")
    lock = Lock.objects.all()[0]
    lock.a, lock.b = not lock.a, not lock.b
    lock.save()

    print("Setting Last-Modified key")
    last_modified_key = "http:headers:Last-Modified:gencache"

    current_timestamp = datetime.now(LOCAL_TIMEZONE).isoformat(
        timespec='seconds'
    )
    redis_conn.set(last_modified_key, current_timestamp)

    # Cache has been run now, so we can delete the key to allow it
    # to be run again in the future.
    redis_conn.delete(running_key)
    print("All done.")


def update_gencache(skip_run_check):
    running_key = "cron:gencache:in_progress"
    redis_conn = redis.Redis(host=settings.REDIS_UCLAPI_HOST,
                             charset="utf-8",
                             decode_responses=True)
    start_time = time.time()
    running = redis_conn.get(running_key)
    if running:
        print("gencache update job already in progress")
        if not skip_run_check:
            return

    redis_conn.set(running_key, "True", ex=2700)

    lock = Lock.objects.all()[0]
    dest_table_index = 2 if lock.a else 1

    # print(dest_table_index)
    # waiting for tasks within a task may lead to deadlocks, use chord and callback
    chord(cache_table_task_testing.s(i, dest_table_index)
          for i in range(len(tables)))(completion_callback.s(running_key,
                                                             start_time))


# https://stackoverflow.com/questions/34830964/how-to-limit-the-maximum-number-of-running-celery-tasks-by-name
@shared_task
def update_gencache_celery(skip_run_check=False):
    try:
        update_gencache(skip_run_check)
    except Exception as gencache_exception:
        print(repr(gencache_exception))
