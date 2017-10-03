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

    timetable_slots = []

    for st_mod in student_modules:
        timetable_slots.extend(Timetable.objects.filter(
            setid=_SETID, moduleid=st_mod.moduleid))

    return(_serialize_timetable(timetable_slots))


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


def _serialize_timetable(timetable_slots):
    serialized, modules, sites, rooms = {}, {}, {}, {}
    for tt_slot in timetable_slots:
        dates = map(lambda k: k.isoformat(), _create_dates(tt_slot))
        for date in dates:
            if date not in serialized:
                serialized[date] = []
            serialized[date].append(_get_event(tt_slot, modules, sites, rooms))
    return serialized


def _get_event(tt_slot, modules, sites, rooms):
    return {
        "start_time": tt_slot.starttime,
        "end_time": tt_slot.finishtime,
        "duration": tt_slot.duration,
        "module": _get_module_details(tt_slot.moduleid, modules),
        "location": _get_location_details(tt_slot.roomid, rooms, sites)
    }


def _get_location_details(roomid, rooms, sites):
    if not roomid: return {}
    if roomid not in rooms:
        room = Rooms.objects.filter(roomid=roomid)[0]
        if room.siteid not in sites:
            sites[room.siteid] = Sites.objects.get(siteid=room.siteid)
        site = sites[room.siteid]
        rooms[roomid] = {
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
    return rooms[roomid]


def _get_module_details(moduleid, modules):
    if not moduleid: return {}
    if moduleid not in modules:
        module = Module.objects.get(moduleid=moduleid, setid=_SETID)
        modules[moduleid] = {
            "name": module.name,
            "module_code": module.linkcode,
            "course_owner": module.owner,
            "module_id": moduleid,
            "lecturer": _get_lecturer_details(module.lecturerid)
        }
    return modules[moduleid]


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
