import datetime

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from .models import Lock, StudentsA, StudentsB, \
    Stumodules, TimetableA, TimetableB, \
    WeekmapnumericA, WeekmapnumericB, \
    WeekstructureA, WeekstructureB, \
    LecturerA, LecturerB, \
    RoomsA, RoomsB, \
    SitesA, SitesB, \
    ModuleA, ModuleB

_SETID = settings.ROOMBOOKINGS_SETID

_week_map = {}
_week_num_date_map = {}

_session_type_map = {
    "L": "Lecture",
    "PBL": "Problem Based Learning",
    "P": "Practical"
}

_rooms_cache = {}

_module_name_cache = {}


def _get_cache(model_name):
    models = {
        "module": [ModuleA, ModuleB],
        "students": [StudentsA, StudentsB],
        "timetable": [TimetableA, TimetableB],
        "weekmapnumeric": [WeekmapnumericA, WeekmapnumericB],
        "weekstructure": [WeekstructureA, WeekstructureB],
        "lecturer": [LecturerA, LecturerB],
        "rooms": [RoomsA, RoomsB],
        "sites": [SitesA, SitesB]
    }
    lock = Lock.objects.all()[0]
    model = models[model_name][0] if lock.a else models[model_name][1]
    return model


def _get_student_by_upi(upi):
    print("Getting student by UPI: " + upi)
    students = _get_cache("students")
    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )[0]
    print("Got student")
    return student


def _get_student_modules(student):
    print("Getting student modules for student: " + student.qtype2)
    raw_query = 'SELECT * FROM CMIS_OWNER.STUMODULES WHERE SETID=\'LIVE-17-18\' AND studentid=\'{}\''.format(  # NOQA
        student.studentid
    )
    student_modules = list(Stumodules.objects.raw(raw_query))
    print("Got student modules for student: " + student.qtype2)
    return student_modules


def _get_lecturer_details(lecturer_upi):
    lecturers = _get_cache("lecturer")
    details = {
        "name": "unknown",
        "email": "unknown"
    }
    try:
        lecturer = lecturers.objects.get(lecturerid=lecturer_upi)
        details["name"] = lecturer.name
        details["email"] = lecturer.linkcode + "@ucl.ac.uk"
    except ObjectDoesNotExist:
        pass

    return details


def _get_timetable_events(student_modules):
    print("Getting timetabled events")
    if not _week_map:
        _map_weeks()

    timetable = _get_cache("timetable")
    modules = _get_cache("module")

    student_timetable = {}
    for module in student_modules:
        print("Getting data for Module ID " + module.moduleid)
        events_data = timetable.objects.filter(
            moduleid=module.moduleid,
            modgrpcode=module.modgrpcode
        )
        for event in events_data:
            for date in _get_real_dates(event):
                date_str = date.strftime("%Y-%m-%d")
                event_data = {
                    "start_time": event.starttime,
                    "end_time": event.finishtime,
                    "duration": event.duration,
                    "module": {
                        "module_code": event.linkcode,
                        "module_id": event.moduleid,
                        "course_owner": event.owner,
                        "lecturer": _get_lecturer_details(event.lecturerid),
                        "name": "Unknown"
                    },
                    "location": _get_location_details(
                        event.siteid,
                        event.roomid
                    ),
                    "session_type": event.moduletype,
                    "session_type_str": _get_session_type_str(
                        event.moduletype
                    ),
                    "session_group": module.modgrpcode
                }

                if event.moduleid not in _module_name_cache:
                    try:
                        module_data = modules.objects.get(
                            moduleid=event.moduleid
                        )
                        _module_name_cache[event.moduleid] = module_data.name
                    except ObjectDoesNotExist:
                        _module_name_cache[event.moduleid] = "Unknown"

                event_data["module"]["name"] = _module_name_cache[
                    event.moduleid
                ]
                if date_str not in student_timetable:
                    student_timetable[date_str] = []
                student_timetable[date_str].append(event_data)
    print("Got timetabled events")
    return student_timetable


def _get_timetable_events_module_list(module_list):
    if not _week_map:
        _map_weeks()

    timetable = _get_cache("timetable")
    modules = _get_cache("module")

    full_modules = []

    for module in module_list:
        try:
            full_modules.append(modules.objects.get(moduleid=module))
        except ObjectDoesNotExist:
            return False

    returned_timetable = {}
    for module in full_modules:
        events_data = timetable.objects.filter(
            moduleid=module.moduleid
        )
        print("Count of events data:")
        print(events_data.count())
        for event in events_data:
            print(event)
            for date in _get_real_dates(event):
                print(date)
                date_str = date.strftime("%Y-%m-%d")
                event_data = {
                    "start_time": event.starttime,
                    "end_time": event.finishtime,
                    "duration": event.duration,
                    "module": {
                        "module_code": event.linkcode,
                        "module_id": event.moduleid,
                        "course_owner": event.owner,
                        "lecturer": _get_lecturer_details(event.lecturerid),
                        "name": module.name
                    },
                    "location": _get_location_details(
                        event.siteid,
                        event.roomid
                    ),
                    "session_type": event.moduletype,
                    "session_type_str": _get_session_type_str(
                        event.moduletype
                    ),
                    "session_group": event.modgrpcode
                }
                if date_str not in returned_timetable:
                    returned_timetable[date_str] = []
                returned_timetable[date_str].append(event_data)
    return returned_timetable


def _map_weeks():
    print("Mapping weeks")
    weekmapnumeric = _get_cache("weekmapnumeric")
    weekstructure = _get_cache("weekstructure")
    week_nums = weekmapnumeric.objects.all()
    week_strs = weekstructure.objects.all()

    for week in week_strs:
        _week_num_date_map[week.weeknumber] = week.startdate

    for week in week_nums:
        if week.weekid not in _week_map:
            _week_map[week.weekid] = []
        _week_map[week.weekid].append(week.weeknumber)
    print("Weeks mapped successfully")


def _get_real_dates(slot):
    return [
        _week_num_date_map[startdate] + datetime.timedelta(
            days=slot.weekday - 1
        )
        for startdate in _week_map[slot.weekid]
    ]


def _get_session_type_str(session_type):
    if session_type in _session_type_map:
        return _session_type_map[session_type]
    else:
        return "Unknown"


def _get_location_details(siteid, roomid):
    if not roomid:
        return {}
    if not siteid:
        return {}

    cache_id = siteid + "___" + roomid
    if cache_id not in _rooms_cache:
        rooms = _get_cache("rooms")
        sites = _get_cache("sites")
        try:
            room = rooms.objects.filter(roomid=roomid, siteid=siteid)[0]
            site = sites.objects.filter(siteid=siteid)[0]
        except IndexError:
            return {}
        _rooms_cache[cache_id] = {
            "name": room.name,
            "capacity": room.capacity,
            "type": room.type,
            "address": [
                site.address1,
                site.address2,
                site.address3
            ],
            "site_name": site.sitename
        }
    return _rooms_cache[cache_id]


def get_student_timetable(upi, date_filter=None):
    print("*** GETTING STUDENT TIMETABLE FOR UPI " + upi + " ***")
    student = _get_student_by_upi(upi)
    print("Getting modules....")
    student_modules = _get_student_modules(student)
    print("Getting events...")
    student_events = _get_timetable_events(student_modules)
    print("Returning events...")
    if date_filter:
        if date_filter in student_events:
            filtered_student_events = {
                date_filter: student_events[date_filter]
            }
        else:
            filtered_student_events = {
                date_filter: []
            }
        return filtered_student_events
    return student_events


def get_custom_timetable(modules, date_filter=None):
    events = _get_timetable_events_module_list(modules)
    if events:
        if date_filter:
            if date_filter in events:
                filtered_events = {
                    date_filter: events[date_filter]
                }
            else:
                filtered_events = {
                    date_filter: []
                }
            return filtered_events
        return events
    return None
