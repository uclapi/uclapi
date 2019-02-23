import redis

from datetime import datetime

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections

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

class Command(BaseCommand):

    help = 'Clones timetable and booking related dbs to speed up queries'

    def handle(self, *args, **options):
        """
        Table format
        (
            Oracle Table Model,
            Bucket A Model,
            Bucket B Model,
            Whether the table has a Set ID field,
            Whether the table is part of the roombookings app
                (i.e. if True: Roombookings, if False: Timetable)
        )
        """
        tables = [
            (Booking, BookingA, BookingB, True, True),
            (Cminstances, CminstancesA, CminstancesB, True, False),
            (Course, CourseA, CourseB, True, False),
            (Depts, DeptsA, DeptsB, False, False),
            (Lecturer, LecturerA, LecturerB, True, False),
            (Module, ModuleA, ModuleB, True, False),
            (Room, RoomA, RoomB, True, True),
            (Sites, SitesA, SitesB, True, False),
            (Stuclasses, StuclassesA, StuclassesB, True, False),
            (Stumodules, StumodulesA, StumodulesB, True, False),
            (Students, StudentsA, StudentsB, True, False),
            (Timetable, TimetableA, TimetableB, True, False),
            (Modulegroups, ModulegroupsA, ModulegroupsB, True, False),
            (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, True, False),
            (Weekmapstring, WeekmapstringA, WeekmapstringB, True, False),
            (Weekstructure, WeekstructureA, WeekstructureB, True, False),
        ]

        lock = Lock.objects.all()[0]
        destination_table_index = 2 if lock.a else 1

        for table_data in tables:
            # Only pulls in objects which apply to this year's Set ID
            if table_data[3]:
                objs = table_data[0].objects.filter(
                    setid=settings.ROOMBOOKINGS_SETID
                )
            else:
                objs = table_data[0].objects.all()

            total_records = objs.count()

            print("Inserting contents of {} into {} [{} records]...".format(
                table_data[0].__name__,
                table_data[destination_table_index].__name__,
                total_records
            ))
            
            # Choose the bucket to be updated
            new_objs = []
            for obj in objs:
                new_objs.append(table_data[destination_table_index](
                    **dict(
                        map(lambda k: (k, getattr(obj, k)),
                            map(lambda l: l.name, obj._meta.get_fields())))
                ))

            cursor = connections['gencache'].cursor()
            table_prefix = "timetable_"
            if table_data[4]:
                table_prefix = "roombookings_"
            cursor.execute(
                "TRUNCATE TABLE {}{} RESTART IDENTITY;".format(
                        table_prefix,
                        table_data[destination_table_index].__name__.lower()
                )
            )

            table_data[destination_table_index].objects.using(
                'gencache'
            ).bulk_create(new_objs, batch_size=5000)

        print("Inverting lock")
        lock.a, lock.b = not lock.a, not lock.b
        lock.save()
        print("Connecting to Redis")
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        print("Setting Last-Modified key")
        last_modified_key = "http:headers:Last-Modified:gencache"

        current_timestamp = datetime.now(LOCAL_TIMEZONE).isoformat(
            timespec='seconds'
        )
        self._redis.set(last_modified_key, current_timestamp)

        call_command('trigger_webhooks')
