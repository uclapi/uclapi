import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from common.helpers import PrettyJsonResponse as JsonResponse

from .models import Stumodules, TimetableA, TimetableB, ModuleA, ModuleB, \
    WeekstructureA, WeekstructureB, WeekmapnumericA, WeekmapnumericB, \
    LecturerA, LecturerB, RoomsA, RoomsB, SitesA, SitesB, Crscompmodules, \
    Crsavailmodules, Lock

_SETID = settings.ROOMBOOKINGS_SETID

week_map = {}
week_num_date_map = {}


def get_timetable(student):
    # To avoid hitting database multiple times.
    if not week_map:
        _map_weeks()
    student_modules = Stumodules.objects.filter(studentid=student.studentid)

    timetable_slots = []
    lock = Lock.objects.all()[0]
    TT = TimetableA if lock.a else TimetableB
    for st_mod in student_modules:
        timetable_slots.extend(
            TT.objects.filter(
                moduleid=st_mod.moduleid,
                modgrpcode=st_mod.modgrpcode
            )
        )

    return _serialize_timetable(timetable_slots)


def get_modules(modules):
    # To avoid hitting database multiple times.
    if not week_map:
        _map_weeks()
    timetable_slots = []
    lock = Lock.objects.all()[0]
    TT = TimetableA if lock.a else TimetableB
    for moduleid in modules:
        timetable_slots.extend(TT.objects.filter(
            setid=_SETID, moduleid=moduleid))
    return _serialize_timetable(timetable_slots)


def get_all_course_modules(courseid):
    compulsary_modules = Crscompmodules.objects.filter(
        setid=_SETID, courseid=courseid)
    available_modules = Crsavailmodules.objects.filter(
        setid=_SETID, courseid=courseid)

    ret_modules = {"compulsary": [], "available": []}

    modules, lecturers = {}, {}

    for module in compulsary_modules:
        ret_modules["compulsary"].append(
            _get_module_details(module.moduleid, modules, lecturers))

    for module in available_modules:
        ret_modules["available"].append(
            _get_module_details(module.moduleid, modules, lecturers))
    return ret_modules


def _map_weeks():
    lock = Lock.objects.all()[0]
    WMN = WeekmapnumericA if lock.a else WeekmapnumericB
    WS = WeekstructureA if lock.a else WeekstructureB
    week_nums = WMN.objects.filter(setid=_SETID)
    week_strs = WS.objects.filter(setid=_SETID)

    for wk in week_strs:
        week_num_date_map[wk.weeknumber] = wk.startdate

    for wk in week_nums:
        if wk.weekid not in week_map:
            week_map[wk.weekid] = []
        week_map[wk.weekid].append(wk.weeknumber)


def _serialize_timetable(timetable_slots):
    serialized, modules, sites, rooms, lecturers = {}, {}, {}, {}, {}
    for tt_slot in timetable_slots:
        dates = map(lambda k: k.isoformat(), _create_dates(tt_slot))
        for date in dates:
            if date not in serialized:
                serialized[date] = []
            serialized[date].append(_get_event(
                tt_slot, modules, sites, rooms, lecturers))
    return serialized


def _get_event(tt_slot, modules, sites, rooms, lecturers):
    return {
        "start_time": tt_slot.starttime + ":00",
        "end_time": tt_slot.finishtime + ":00",
        "duration": tt_slot.duration,
        "module": _get_module_details(tt_slot.moduleid, modules, lecturers),
        "location": _get_location_details(tt_slot.roomid, rooms, sites)
    }


def _get_location_details(roomid, rooms, sites):
    if not roomid:
        return {}
    if roomid not in rooms:
        lock = Lock.objects.all()[0]
        R = RoomsA if lock.a else RoomsB
        room = R.objects.filter(roomid=roomid)[0]
        if room.siteid not in sites:
            S = SitesA if lock.a else SitesB
            sites[room.siteid] = S.objects.filter(siteid=room.siteid)[0]
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


def _get_module_details(moduleid, modules, lecturers):
    if not moduleid:
        return {}
    if moduleid not in modules:
        lock = Lock.objects.all()[0]
        M = ModuleA if lock.a else ModuleB
        module = M.objects.get(moduleid=moduleid, setid=_SETID)
        modules[moduleid] = {
            "name": module.name,
            "module_code": module.linkcode,
            "course_owner": module.owner,
            "module_id": moduleid,
            "lecturer": _get_lecturer_details(module.lecturerid, lecturers)
        }
    return modules[moduleid]


def _get_lecturer_details(lecturerid, lecturers):
    if not lecturerid:
        return {}
    if lecturerid not in lecturers:
        lock = Lock.objects.all()[0]
        L = LecturerA if lock.a else LecturerB
        lecturer = L.objects.get(lecturerid=lecturerid, setid=_SETID)
        lecturers[lecturerid] = {
            "name": lecturer.name,
            "email": lecturer.linkcode + "@ucl.ac.uk"
            if lecturer.linkcode else ""
        }
    return lecturers[lecturerid]


def _create_dates(tt_slot):
    return [
        week_num_date_map[startdate]
        + datetime.timedelta(days=tt_slot.weekday - 1)
        for startdate in week_map[tt_slot.weekid]
    ]
