import gc

import django
import redis

import time

from datetime import datetime
from multiprocessing import Pool

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from tqdm import tqdm
from django import db


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
    Crsavailmodules, CrsavailmodulesA, CrsavailmodulesB, \
    Crscompmodules, CrscompmodulesA, CrscompmodulesB, \
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


def cache_table_process(index, destination_table_index, options):
    # Number of objects to load into RAM at once from Oracle
    # when chunking.
    load_batch_size = 10000
    # Maxmimum number of objects to insert into PostgreSQL
    # at once.
    insert_batch_size = 5000

    table_data = tables[index]

    # Delete existing cached data
    gencache_cursor = connections['gencache'].cursor()
    table_prefix = "roombookings_" if table_data[4] else "timetable_"
    gencache_cursor.execute(
        "TRUNCATE TABLE {}{} RESTART IDENTITY;".format(
                table_prefix,
                table_data[destination_table_index].__name__.lower()
        )
    )

    # Decide whether to use a chunked query or not
    if table_data[5]:
        oracle_cursor = connections['roombookings'].cursor()
        if table_data[3]:
            query = "SELECT COUNT(SETID) FROM {} WHERE SETID = '{}'".format(
                table_data[0]._meta.db_table,
                settings.ROOMBOOKINGS_SETID
            )
        else:
            query = "SELECT COUNT(*) FROM {}".format(
                table_data[0]._meta.db_table
            )

        oracle_cursor.execute(query)
        count_data = oracle_cursor.fetchone()
        total_records = count_data[0]

        if table_data[3]:
            query = "SELECT * FROM {} WHERE SETID = '{}'".format(
                table_data[0]._meta.db_table,
                settings.ROOMBOOKINGS_SETID
            )
        else:
            query = "SELECT * FROM {}".format(
                table_data[0]._meta.db_table
            )

        oracle_cursor.arraysize = load_batch_size

        oracle_cursor.execute(query)

        def columns(cursor):
            return {cd[0]: i for i, cd in enumerate(cursor.description)}
        cols = columns(oracle_cursor)

        if options['unattended']:
            print("[Start] Chunk caching from {} [{} records]".format(
                table_data[0].__name__,
                total_records
            ))
        else:
            progress_title = "Chunk caching from {} [{} records]".format(
                table_data[0].__name__,
                total_records
            )
            prog = tqdm(
                desc=progress_title,
                position=index + 1,
                total=total_records
            )
            prog.update(0)

        new_objs = []
        objs = oracle_cursor.fetchmany(load_batch_size)
        while objs:
            for obj in objs:
                new_obj = {}
                for k, v in cols.items():
                    if obj[v]:
                        val = obj[v]
                    else:
                        if isinstance(obj[v], str):
                            val = ''
                        elif isinstance(obj[v], int):
                            val = 0
                        else:
                            val = None
                    new_obj[k.lower()] = val

                new_objs.append(table_data[destination_table_index](**new_obj))

                if not options['unattended']:
                    prog.update(1)

                if len(new_objs) >= load_batch_size:
                    table_data[destination_table_index].objects.using(
                        'gencache'
                    ).bulk_create(new_objs, batch_size=insert_batch_size)
                    new_objs.clear()
                    gc.collect()

            objs = oracle_cursor.fetchmany(load_batch_size)

        # Insert any items left over
        table_data[destination_table_index].objects.using(
            'gencache'
        ).bulk_create(new_objs, batch_size=insert_batch_size)
        del new_objs
        oracle_cursor.close()
        if options['unattended']:
            print("[Done!] Chunk caching from {} [{} records]".format(
                table_data[0].__name__,
                total_records
            ))
    else:
        if table_data[3]:
            objs = table_data[0].objects.filter(
                setid=settings.ROOMBOOKINGS_SETID
            )
        else:
            objs = table_data[0].objects.all()

        new_objs = []
        item_count = objs.count()
        if options['unattended']:
            print("[Start] Loading {} into RAM [{} records]".format(
                table_data[0].__name__,
                item_count
            ))
        else:
            ram_load_header = "Loading {} into RAM [{} records]".format(
                table_data[0].__name__,
                item_count
            )

            prog = tqdm(
                desc=ram_load_header,
                position=index + 1,
                total=item_count
            )
            prog.update(0)

        for obj in objs:
            new_objs.append(table_data[destination_table_index](
                **dict(
                    map(lambda k: (k, getattr(obj, k)),
                        map(lambda l: l.name, obj._meta.get_fields())))
            ))
            if not options['unattended']:
                prog.update(1)

        if not options['unattended']:
            prog.close()

        table_data[destination_table_index].objects.using(
            'gencache'
        ).bulk_create(new_objs, batch_size=insert_batch_size)
        new_objs.clear()
        del new_objs
        del objs

        if options['unattended']:
            print("[Done!] Loading {} into RAM [{} records]".format(
                table_data[0].__name__,
                item_count
            ))

    gc.collect()
    db.reset_queries()


class Command(BaseCommand):
    help = 'Clones databases from Oracle into PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--unattended',
            action='store_true',
            dest='unattended',
            default=False,
            help='Run in unattended mode designed to be piped into a log file'
        )

        parser.add_argument(
            '--skip-run-check',
            action='store_true',
            dest='skip_run_check',
            default=False,
            help=(
                'The gencache task will run even if there is still a job '
                'in progress according to Redis'
            )
        )

    def handle(self, *args, **options):
        start_time = time.time()
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
            # Only quit if we haven't specified that we want to override
            # this check
            if not options['skip_run_check']:
                return

        # There is no other job running so we can cache now
        # We set the TTL to 2700 seconds = 45 minutes, the maximum time
        # that the cache operation could ever take before we consider it
        # to have died or failed.
        self._redis.set(cache_running_key, "True", ex=2700)

        lock = Lock.objects.all()[0]
        destination_table_index = 2 if lock.a else 1

        with Pool(processes=2) as pool:
            # Build up a list of argument tuples for the child process calls
            pool_args = []
            for i in range(0, len(tables)):
                pool_args.append((i, destination_table_index, options))

            pool.starmap(cache_table_process, pool_args)

            pool.close()
            pool.join()
        for i in tables:
            print()

        print()
        elapsed_time = time.time() - start_time
        print(
            "Caching process completed in {}m {}s".format(
                int(elapsed_time // 60),
                int(elapsed_time % 60)
            )
        )

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
