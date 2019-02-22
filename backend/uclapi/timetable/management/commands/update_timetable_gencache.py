from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from datetime import datetime
import redis
from common.helpers import LOCAL_TIMEZONE
from timetable.models import \
    Timetable, TimetableA, TimetableB, \
    Weekstructure, WeekstructureA, WeekstructureB, \
    Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, \
    Lecturer, LecturerA, LecturerB, \
    Rooms, RoomsA, RoomsB, \
    Sites, SitesA, SitesB, \
    Module, ModuleA, ModuleB, \
    Weekmapstring, WeekmapstringA, WeekmapstringB, \
    Students, StudentsA, StudentsB, \
    Depts, DeptsA, DeptsB, \
    Cminstances, CminstancesA, CminstancesB, \
    Stumodules, StumodulesA, StumodulesB, \
    Modulegroups, ModulegroupsA, ModulegroupsB, \
    Course, CourseA, CourseB, \
    Stuclasses, StuclassesA, StuclassesB, \
    Lock


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def handle(self, *args, **options):
        # Table format: (OracleTable, BucketA, BucketB, HasSetID)
        tables = [
            (Module, ModuleA, ModuleB, True),
            (Timetable, TimetableA, TimetableB, True),
            (Weekstructure, WeekstructureA, WeekstructureB, True),
            (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, True),
            (Weekmapstring, WeekmapstringA, WeekmapstringB, True),
            (Lecturer, LecturerA, LecturerB, True),
            (Rooms, RoomsA, RoomsB, True),
            (Sites, SitesA, SitesB, True),
            (Students, StudentsA, StudentsB, True),
            (Depts, DeptsA, DeptsB, False),
            (Cminstances, CminstancesA, CminstancesB, True),
            (Stumodules, StumodulesA, StumodulesB, True),
            (Modulegroups, ModulegroupsA, ModulegroupsB, True),
            (Course, CourseA, CourseB, True),
            (Stuclasses, StuclassesA, StuclassesB, True),
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
            cursor.execute(
                "TRUNCATE TABLE timetable_{} RESTART IDENTITY;".format(
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
        last_modified_key = "http:headers:Last-Modified:timetable_gencache"

        current_timestamp = datetime.now(LOCAL_TIMEZONE).isoformat(
            timespec='seconds'
        )
        self._redis.set(last_modified_key, current_timestamp)
