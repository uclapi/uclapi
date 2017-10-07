import os

from django.core.management.base import BaseCommand
from django.conf import settings

from timetable.models import Timetable, TimetableA, TimetableB, \
    Weekstructure, WeekstructureA, WeekstructureB, \
    Weekmapnumeric, WeekmapnumericA, WeekmapnumericB, \
    Lecturer, LecturerA, LecturerB, \
    Rooms, RoomsA, RoomsB, \
    Sites, SitesA, SitesB, \
    Timetable, TimetableA, TimetableB, \
    Module, ModuleA, ModuleB, \
    Weekmapstring, WeekmapstringA, WeekmapstringB, \
    Lock


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def handle(self, *args, **options):
        classes = [
            (Module, ModuleA, ModuleB),
            (Timetable, TimetableA, TimetableB),
            (Weekstructure, WeekstructureA, WeekstructureB),
            (Weekmapnumeric, WeekmapnumericA, WeekmapnumericB),
            (Weekmapstring, WeekmapstringA, WeekmapstringB),
            (Lecturer, LecturerA, LecturerB),
            (Rooms, RoomsA, RoomsB),
            (Sites, SitesA, SitesB),
        ]

        lock = Lock.objects.all()[0]
        tbu = 1 if lock.a else 2

        for c in classes:
            # get all current year objects
            objs = c[0].objects.filter(setid=settings.ROOMBOOKINGS_SETID)
            # choose the bucket to be updated.
            new_objs = []
            for obj in objs:
                new_objs.append(c[tbu](
                    **dict(
                        map(lambda k: (k, getattr(obj, k)),
                            map(lambda l: l.name, obj._meta.get_fields())))
                ))
            c[tbu].objects.all().delete()
            c[tbu].objects.using('gencache').bulk_create(
                new_objs,
                batch_size=5000
            )
        lock.a, lock.b = not lock.a, not lock.b
        lock.save()
