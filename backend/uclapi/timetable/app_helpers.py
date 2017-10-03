from roombookings.helpers import PrettyJsonResponse as JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Stumodules, Timetable, Module, Weekstructure, \
    Weekmapnumeric, Lecturer, Rooms, Sites
from django.conf import settings
import datetime

_SETID = settings.ROOMBOOKINGS_SETID

week_map = {}
week_num_date_map = {}


def get_timetable(student):
    # To avoid hitting database multiple times.
    if not week_map:
        _map_weeks()
    student_modules = Stumodules.objects.filter(
        setid=_SETID, studentid=student.studentid)

    timetable_slots, modules = [], {}

    for st_mod in student_modules:
        timetable_slots.extend(Timetable.objects.filter(
            setid=_SETID, moduleid=st_mod.moduleid))
        modules[st_mod.moduleid] = Module.objects.filter(
            setid=_SETID, moduleid=st_mod.moduleid)[0]

    return(_serialize_timetable(timetable_slots, modules))


def _map_weeks():
    week_nums = Weekmapnumeric.objects.filter(setid=_SETID)
    week_strs = Weekstructure.objects.filter(setid=_SETID)

    tmp_map = {}

    for wk in week_strs:
        week_num_date_map[wk.weeknumber] = wk.startdate

    for wk in week_nums:
        if wk.weekid not in week_map:
            week_map[wk.weekid] = []
        week_map[wk.weekid].append(wk.weeknumber)


def _serialize_timetable(timetable_slots, modules):
    serialized = {}
    for tt_slot in timetable_slots:
        dates = map(lambda k: k.isoformat(), _create_dates(tt_slot))
        for date in dates:
            if date not in serialized:
                serialized[date] = []
            serialized[date].append(_get_event(tt_slot, modules))
    return serialized


def _get_event(tt_slot, modules):
    return {
        "start_time": tt_slot.starttime,
        "end_time": tt_slot.finishtime,
        "duration": tt_slot.duration,
        "module": _get_module_details(tt_slot.moduleid, modules),
        "location": _get_location_details(tt_slot.roomid)
    }


def _get_location_details(roomid):
    if not roomid: return {}
    room = Rooms.objects.filter(roomid=roomid)[0]
    site = Sites.objects.get(siteid=room.siteid)
    return {
        "name": room.name,
        "capacity": room.capacity,
        "type": room.type,
        "address": [
            site.address1,
            site.address2,
            site.address3
        ],
        "sitename": site.sitename
    }


def _get_module_details(moduleid, modules):
    if not moduleid: return {}
    try:
        module = modules[moduleid]
    except KeyError:
        return {}
    return {
        "name": module.name,
        "module_code": module.linkcode,
        "course_owner": module.owner,
        "module_id": moduleid,
        "lecturer": _get_lecturer_details(module.lecturerid)
    }


def _get_lecturer_details(lecturerid):
    if not lecturerid: return {}
    lecturer = Lecturer.objects.get(lecturerid=lecturerid)
    return {
        "name": lecturer.name,
        "email": lecturer.linkcode + "@ucl.ac.uk" if lecturer.linkcode else ""
    }


def _create_dates(tt_slot):
    return [
        week_num_date_map[startdate]
        + datetime.timedelta(days=(tt_slot.weekday - 1))
        for startdate in week_map[tt_slot.weekid]
    ]
