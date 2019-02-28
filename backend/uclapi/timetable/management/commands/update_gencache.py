import copy
import gc
import multiprocessing
import sys

import redis

from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from django.db import connections

import django
# Nasty hack to ensure we can initialise models in worker processes
# Courtesy of: https://stackoverflow.com/a/39996838
if not apps.ready and not settings.configured:
    django.setup()

from common.helpers import LOCAL_TIMEZONE
from roombookings.models import \
    Room, RoomA, RoomB, \
    Booking, BookingA, BookingB
from timetable.models import \
    Cminstances, CminstancesA, CminstancesB, \
    Course, CourseA, CourseB, \
    Depts, DeptsA, DeptsB, \
    Lecturer, LecturerA, LecturerB, \
    Module, ModuleA, ModuleB, \
    Modulegroups, ModulegroupsA, ModulegroupsB, \
    Sites, SitesA, SitesB, \
    Stuclasses, StuclassesA, StuclassesB, \
    Stumodules, StumodulesA, StumodulesB, \
    Students, StudentsA, StudentsB, \
    Timetable, TimetableA, TimetableB, \
    Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, \
    Weekmapstring, WeekmapstringA, WeekmapstringB, \
    Weekstructure, WeekstructureA, WeekstructureB, \
    Lock


"""
    Table format
    (
        Oracle Table Model,
        Bucket A Model,
        Bucket B Model,
        Whether the table has a Set ID field,
        Whether the table is part of the roombookings app
            (i.e. if True: Roombookings, if False: Timetable),
        Whether the source table should be fetched in chunks
            (i.e. if True: chunking, if False: fetched all at once)
    )
    """
tables = [
    (Booking, BookingA, BookingB, True, True, True),
    (Cminstances, CminstancesA, CminstancesB, True, False, False),
    (Course, CourseA, CourseB, True, False, False),
    (Depts, DeptsA, DeptsB, False, False, False),
    (Lecturer, LecturerA, LecturerB, True, False, True),
    (Module, ModuleA, ModuleB, True, False, False),
    (Room, RoomA, RoomB, True, True, False),
    (Sites, SitesA, SitesB, True, False, False),
    (Stuclasses, StuclassesA, StuclassesB, True, False, False),
    (Stumodules, StumodulesA, StumodulesB, True, False, False),
    (Students, StudentsA, StudentsB, True, False, True),
    (Timetable, TimetableA, TimetableB, True, False, True),
    (Modulegroups, ModulegroupsA, ModulegroupsB, True, False, True),
    (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, True, False, False),
    (Weekmapstring, WeekmapstringA, WeekmapstringB, True, False, False),
    (Weekstructure, WeekstructureA, WeekstructureB, True, False, False),
]


# Another Stack Exchange solution!
# https://blender.stackexchange.com/a/30739
def update_progress(job_title, progress):
    length = 30
    block = int(round(length * progress))
    msg = "\r{0}: [{1}] {2}%".format(
        job_title,
        "#"*block + "-"*(length - block),
        round(progress * 100, 2)
    )
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


# More efficient QuerySet iterator that won't kill our RAM usage
# https://stackoverflow.com/a/5188179
class FriendlyQuerySetIterator(object):
    def __init__(self, queryset, object_limit):
        self._queryset = queryset
        self._generator = self._setup()
        self.object_limit = object_limit

    def _setup(self):
        record_count = self._queryset.count()
        progress_title = "Chunk caching [{} records]".format(
            record_count
        )
        for i in range(0, record_count, self.object_limit):
            update_progress(progress_title, i / record_count)
            gc.collect()
            # By making a copy of of the queryset and using that to actually access
            # the objects we ensure that there are only object_limit objects in
            # memory at any given time
            sub_queryset = copy.deepcopy(self._queryset)[i:i + self.object_limit]
            for obj in sub_queryset.iterator():
                yield obj

        # When complete
        update_progress(progress_title, 1)

    def __iter__(self):
        return self

    def __next__(self):
        return self._generator.__next__()


def cache_table_process(index, destination_table_index):
     # Number of objects to load into RAM at once from Oracle when chunking.
    load_batch_size = 20000
    # Maxmimum number of objects to insert into PostgreSQL at once.
    insert_batch_size = 40000

    table_data = tables[index]

    # Only pulls in objects which apply to this year's Set ID
    if table_data[3]:
        objs = table_data[0].objects.filter(
            setid=settings.ROOMBOOKINGS_SETID
        )
    else:
        objs = table_data[0].objects.all()

    print("Inserting contents of {} into {}...".format(
        table_data[0].__name__,
        table_data[destination_table_index].__name__
    ))

    cursor = connections['gencache'].cursor()

    table_prefix = "roombookings_" if table_data[4] else "timetable_"

    cursor.execute(
        "TRUNCATE TABLE {}{} RESTART IDENTITY;".format(
                table_prefix,
                table_data[destination_table_index].__name__.lower()
        )
    )

    # Decide whether to use a chunked query or not
    if table_data[5]:
        new_objs = []
        for obj in FriendlyQuerySetIterator(objs, load_batch_size):
            new_objs.append(table_data[destination_table_index](
                **dict(
                    map(lambda k: (k, getattr(obj, k)),
                        map(lambda l: l.name, obj._meta.get_fields())))
            ))
            if len(new_objs) >= load_batch_size:
                table_data[destination_table_index].objects.using(
                    'gencache'
                ).bulk_create(new_objs, batch_size=insert_batch_size)
                new_objs.clear()

        # Insert any items left over
        table_data[destination_table_index].objects.using(
            'gencache'
        ).bulk_create(new_objs, batch_size=insert_batch_size)
    else:
        new_objs = []
        item_count = objs.count()
        ram_load_header = "Loading {} into RAM [{} records]".format(
            table_data[0].__name__,
            item_count
        )
        update_progress(ram_load_header, 0)
        for obj in objs:
            new_objs.append(table_data[destination_table_index](
                **dict(
                    map(lambda k: (k, getattr(obj, k)),
                        map(lambda l: l.name, obj._meta.get_fields())))
            ))
            if len(new_objs) % load_batch_size == 0:
                update_progress(ram_load_header, len(new_objs) / item_count)
        update_progress(ram_load_header, 1)
        print("Now batch inserting into PostgreSQL (this may take some time)...")
        table_data[destination_table_index].objects.using(
            'gencache'
        ).bulk_create(new_objs, batch_size=insert_batch_size)


class Command(BaseCommand):
    help = 'Clones timetable and booking related databases from Oracle into PostgreSQL'

    def handle(self, *args, **options):
        # We first check if we are already caching so that we don't
        # tread over ourselves by trying to cache twice at once
        print("Connecting to Redis")
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )

        cache_running_key = "cron:gencache:in_progress"
        running = self._redis.get(cache_running_key)
        if running:
            print("## A gencache update job is still in progress ##")
            return

        # There is no other job running so we can cache now
        # We set the TTL to 2700 seconds = 45 minutes, the maximum time
        # that the cache operation could ever take before we consider it
        # to have died or failed.
        self._redis.set(cache_running_key, "True", ex=2700)

        lock = Lock.objects.all()[0]
        destination_table_index = 2 if lock.a else 1

        for i in range(0, len(tables)):
            p = multiprocessing.Process(
                target=cache_table_process,
                args=(i, destination_table_index,)
            )
            p.start()
            p.join()

        print("Inverting lock")
        lock.a, lock.b = not lock.a, not lock.b
        lock.save()

        print("Setting Last-Modified key")
        last_modified_key = "http:headers:Last-Modified:gencache"

        current_timestamp = datetime.now(LOCAL_TIMEZONE).isoformat(
            timespec='seconds'
        )
        self._redis.set(last_modified_key, current_timestamp)

        # Cache has been run now, so we can delete the key to allow it
        # to be run again in the future.
        self._redis.delete(cache_running_key)

        call_command('trigger_webhooks')
