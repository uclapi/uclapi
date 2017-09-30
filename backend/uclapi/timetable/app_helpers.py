from roombookings.helpers import PrettyJsonResponse as JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Stumodules, Timetable, Module
from django.conf import settings

_SETID = settings.ROOMBOOKINGS_SETID


def get_timetable(student):
    student_modules = Stumodules.objects.filter(
        setid=_SETID, studentid=student.studentid)

    timetable_slots, modules = [], {}

    for st_mod in student_modules:
        timetable_slots.extend(Timetable.objects.fileter(
            setid=_SETID, moduleid=st_mod.moduleid))
        modules[st_mod.moduleid] = Module.objects.filter(
            setid=_SETID, moduleid=st_mod.moduleid)[0]

    serialised_timetable = _serialize_timetable(timetable_slots, modules)

# 
# def _serialize_timetable(timetable_slots, modules):
#
#     for slot in timetable_slots:
