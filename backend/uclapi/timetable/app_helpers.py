from roombookings.helpers import PrettyJsonResponse as JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Stumodules, Timetable, Module, Weekstructure, Weekmapnumeric
from django.conf import settings
import datetime

_SETID = settings.ROOMBOOKINGS_SETID

week_map = {}


def get_timetable(student):
    # To avoid hitting database multiple times.
    if not week_map:
        _map_weeks()

    student_modules = Stumodules.objects.filter(
        setid=_SETID, studentid=student.studentid)

    timetable_slots, modules = [], {}

    for st_mod in student_modules:
        timetable_slots.extend(Timetable.objects.fileter(
            setid=_SETID, moduleid=st_mod.moduleid))
        modules[st_mod.moduleid] = Module.objects.filter(
            setid=_SETID, moduleid=st_mod.moduleid)[0]

    serialised_timetable = _serialize_timetable(timetable_slots, modules)


def _map_weeks():
    week_nums = Weekmapnumeric.objects.all()
    week_strs = Weekstructure.objects.all()

    tmp_map = {}

    for wk in week_nums:
        tmp_map[wk.weekid] = wk.weeknumber

    tmp_map = dict(zip(tmp_map.values(), tmp_map.keys()))

    for wk in week_strs:
        week_map[tmp_map[wk.weeknumber]] = wk.startdate


def _serialize_timetable(timetable_slots, modules):
    serialized = {}
    for tt_slot in timetable_slots:
        date = create_date(tt_slot).isoformat()
        if date not in serialized:
            serialized[date] = []
        serialized[date].append(_get_event(tt_slot))


def _get_event(tt_slot):
    return {
        "start_time": tt_slot.starttime,
        "end_time": tt_slot.finishtime,
        "duration": tt_slot.duration,
        "module": _get_module_details(tt_slot.moduleid)
    }


def _create_data(tt_slot):
    return Weekstructure.objects.get(weeknumber=week_map[tt_slot.weekid]) +
    datetime.timedelta(days=tt_slot.weekday)
