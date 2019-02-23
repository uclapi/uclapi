from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from datetime import datetime
import redis
from common.helpers import LOCAL_TIMEZONE
from roombookings.models import \
    Room, RoomA, RoomB, \
    Booking, BookingA, BookingB
from timetable.models import \
    Timetable, TimetableA, TimetableB, \
    Weekstructure, WeekstructureA, WeekstructureB, \
    Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, \
    Lecturer, LecturerA, LecturerB, \
    Sites, SitesA, SitesB, \
    Module, ModuleA, ModuleB, \
    Weekmapstring, WeekmapstringA, WeekmapstringB, \
    Students, StudentsA, StudentsB, \
    Depts, DeptsA, DeptsB, \
    Cminstances, CminstancesA, CminstancesB, \
    Stumodules, StumodulesA, StumodulesB, \
    Lock


class Command(BaseCommand):

    help = 'Clones timetable and booking related dbs to speed up queries'

    def handle(self, *args, **options):
        # Table format: (OracleTable, BucketA, BucketB, HasSetID, isBookingsGenCache)
        tables = [
            (Module, ModuleA, ModuleB, True, False),
            (Timetable, TimetableA, TimetableB, True, False),
            (Weekstructure, WeekstructureA, WeekstructureB, True, False),
            (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, True, False),
            (Weekmapstring, WeekmapstringA, WeekmapstringB, True, False),
            (Lecturer, LecturerA, LecturerB, True, False),
            (Sites, SitesA, SitesB, True, False),
            (Students, StudentsA, StudentsB, True, False),
            (Depts, DeptsA, DeptsB, False, False),
            (Cminstances, CminstancesA, CminstancesB, True, False),
            (Stumodules, StumodulesA, StumodulesB, True, False),
            (Room, RoomA, RoomB, True, True),
            (Booking, BookingA, BookingB, True, True)
        ]

        lock = Lock.objects.all()[0]
        destination_table_index = 2 if lock.a else 1

        for table_data in tables:
            print("Inserting contents of {} into {}".format(
                table_data[0].__name__,
                table_data[destination_table_index].__name__
            ))
            # Only pulls in objects which apply to this year's Set ID
            if table_data[3]:
                objs = table_data[0].objects.filter(
                    setid=settings.ROOMBOOKINGS_SETID
                )
            else:
                objs = table_data[0].objects.all()

            # choose the bucket to be updated.
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
