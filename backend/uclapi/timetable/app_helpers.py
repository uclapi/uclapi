import datetime
import json

import redis
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from roombookings.models import (
    Lock as RBLock,
    BookingA,
    BookingB,
    Location,
    SiteLocation
)

from .models import (DeptsA, DeptsB, LecturerA, LecturerB, Lock, ModuleA,
                     ModuleB, RoomsA, RoomsB, SitesA, SitesB, StudentsA,
                     StudentsB, Stumodules, TimetableA, TimetableB,
                     WeekmapnumericA, WeekmapnumericB, WeekstructureA,
                     WeekstructureB)
from .tasks import cache_student_timetable

_SETID = settings.ROOMBOOKINGS_SETID

_week_map = {}
_week_num_date_map = {}

_session_type_map = {
    "EX": "Examination",
    "L": "Lecture",
    "P": "Practical",
    "PBL": "Problem Based Learning",
}

_rooms_cache = {}

_department_name_cache = {}


def _get_cache(model_name):
    """Returns the cache bucket for the requested model name"""
    timetable_models = {
        "module": [ModuleA, ModuleB],
        "students": [StudentsA, StudentsB],
        "timetable": [TimetableA, TimetableB],
        "weekmapnumeric": [WeekmapnumericA, WeekmapnumericB],
        "weekstructure": [WeekstructureA, WeekstructureB],
        "lecturer": [LecturerA, LecturerB],
        "rooms": [RoomsA, RoomsB],
        "sites": [SitesA, SitesB],
        "departments": [DeptsA, DeptsB]
    }
    roombookings_models = {
        "booking": [BookingA, BookingB]
    }
    if model_name in timetable_models:
        timetable_lock = Lock.objects.all()[0]
        if timetable_lock.a:
            model = timetable_models[model_name][0]
        else:
            model = timetable_models[model_name][1]
    elif model_name in roombookings_models:
        roombooking_lock = RBLock.objects.all()[0]
        if roombooking_lock.bookingA:
            model = roombookings_models[model_name][0]
        else:
            model = roombookings_models[model_name][1]
    else:
        raise Exception("Unknown model requested from cache")

    return model


def _get_student_by_upi(upi):
    """Returns a StudentA or StudentB object by UPI"""
    students = _get_cache("students")
    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )[0]
    return student


def _get_student_modules(student):
    """Returns all Stumodules object by for a given student"""
    raw_query = 'SELECT * FROM CMIS_OWNER.STUMODULES WHERE SETID=\'LIVE-17-18\' AND studentid=\'{}\''.format(  # NOQA
        student.studentid
    )
    student_modules = list(Stumodules.objects.raw(raw_query))
    return student_modules


def _get_full_department_name(department_code):
    """Converts a department code, such as COMPS_ENG, into a full name
    such as Computer Science"""
    if department_code in _department_name_cache:
        return _department_name_cache[department_code]
    else:
        departments = _get_cache("departments")
        try:
            dept = departments.objects.get(deptid=department_code)
            _department_name_cache[department_code] = dept.name
            return dept.name
        except ObjectDoesNotExist:
            return "Unknown"


def _get_lecturer_details(lecturer_upi):
    """Returns a lecturer's name and email address from their UPI"""
    lecturers = _get_cache("lecturer")
    details = {
        "name": "Unknown",
        "email": "Unknown",
        "department_id": "Unknown",
        "department_name": "Unknown"
    }
    try:
        lecturer = lecturers.objects.get(lecturerid=lecturer_upi)
    except ObjectDoesNotExist:
        pass

    details["name"] = lecturer.name
    details["email"] = lecturer.linkcode + "@ucl.ac.uk"

    if lecturer.owner:
        details["department_id"] = lecturer.owner
        details["department_name"] = _get_full_department_name(lecturer.owner)

    return details


def _get_timetable_events(full_modules, stumodules):
    """
    Gets a dictionary of timetabled events.
    If stumodules=True then assume full_modules = [Stumodules]
    If stumodules=False then assume full_modules [ModuleA] or [ModuleB]
    """
    if not _week_map:
        _map_weeks()

    timetable = _get_cache("timetable")
    modules = _get_cache("module")

    bookings = _get_cache("booking")

    full_timetable = {}
    for module in full_modules:
        if stumodules:
            # Get events for the lab group assigned
            # Also include general lecture events (via the or operator)
            events_data = timetable.objects.filter(
                Q(modgrpcode=module.modgrpcode) | Q(modgrpcode=''),
                moduleid=module.moduleid
            )
            module_data = modules.objects.get(moduleid=module.moduleid)
        else:
            events_data = timetable.objects.filter(
                moduleid=module.moduleid
            )
            module_data = module
        for event in events_data:
            event_bookings = bookings.objects.filter(slotid=event.slotid)
            if len(event_bookings) == 0:
                # We have to trust the data in the event because
                # no rooms are booked for some weird reason.
                for date in _get_real_dates(event):
                    event_data = {
                        "start_time": event.starttime,
                        "end_time": event.finishtime,
                        "duration": event.duration,
                        "module": {
                            "module_id": module_data.moduleid,
                            "department_id": event.owner,
                            "department_name": _get_full_department_name(
                                event.owner
                            ),
                            "name": module_data.name
                        },
                        "location": _get_location_details(
                            event.siteid,
                            event.roomid
                        ),
                        "session_title": module_data.name,
                        "session_type": event.moduletype,
                        "session_type_str": _get_session_type_str(
                            event.moduletype
                        ),
                        "contact": "Unknown"
                    }

                    # If this is student module data, add in the group code
                    # because we have that field in Stumodules
                    if stumodules:
                        event_data["session_group"] = event.modgrpcode
                        if event.modgrpcode != '':
                            event_data["session_title"] = "{} ({})".format(
                                module_data.name,
                                event.modgrpcode
                            )

                    # Check if the module timetable event's Lecturer ID
                    # exists. If not, we use the Lecturer ID associated
                    # with the module as a whole. It's an ugly hack, but
                    # it works around not all timetabled lectures having
                    # the Lecturer ID field filled as they should.
                    # We assume therefore that if the lecturer isn't
                    # specified then the class is to be led by the
                    # module's owner.
                    if event.lecturerid.strip():
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(event.lecturerid)
                    else:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(module_data.lecturerid)

                    date_str = date.strftime("%Y-%m-%d")
                    if date_str not in full_timetable:
                        full_timetable[date_str] = []
                    full_timetable[date_str].append(event_data)

            else:
                for booking in event_bookings:
                    event_data = {
                        "start_time": booking.starttime,
                        "end_time": booking.finishtime,
                        "duration": event.duration,
                        "module": {
                            "module_id": module_data.moduleid,
                            "department_id": event.owner,
                            "department_name": _get_full_department_name(
                                event.owner
                            ),
                            "name": module_data.name
                        },
                        "location": _get_location_details(
                            booking.siteid,
                            booking.roomid
                        ),
                        "session_title": booking.title,
                        "session_type": event.moduletype,
                        "session_type_str": _get_session_type_str(
                            event.moduletype
                        ),
                        "contact": booking.condisplayname
                    }

                    # If this is student module data, add in the group code
                    # because we have that field in Stumodules
                    if stumodules:
                        event_data["session_group"] = module.modgrpcode

                    # Check if the module timetable event's Lecturer ID
                    # exists. If not, we use the Lecturer ID associated
                    # with the module as a whole. It's an ugly hack, but
                    # it works around not all timetabled lectures having
                    # the Lecturer ID field filled as they should.
                    # We assume therefore that if the lecturer isn't
                    # specified then the class is to be led by the
                    # module's owner.
                    if event.lecturerid.strip():
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(event.lecturerid)
                    else:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(module_data.lecturerid)

                    date_str = booking.startdatetime.strftime("%Y-%m-%d")
                    if date_str not in full_timetable:
                        full_timetable[date_str] = []
                    full_timetable[date_str].append(event_data)
    return full_timetable


def _get_timetable_events_module_list(module_list):
    if not _week_map:
        _map_weeks()

    modules = _get_cache("module")

    full_modules = []

    for module in module_list:
        try:
            full_modules.append(modules.objects.get(moduleid=module))
        except ObjectDoesNotExist:
            return False

    return _get_timetable_events(full_modules, False)


def _map_weeks():
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


def _get_location_coordinates(siteid, roomid):
    # First try and get the specific room's location
    try:
        location = Location.objects.get(
            siteid=siteid,
            roomid=roomid
        )
        return location.lat, location.lng
    except Location.DoesNotExist:
        pass

    # Now try and get the building's location
    try:
        location = SiteLocation.objects.get(
            siteid=siteid
        )
        return location.lat, location.lng
    except SiteLocation.DoesNotExist:
        pass

    # Now just bail
    return None, None


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
        lat, lng = _get_location_coordinates(siteid, roomid)
        _rooms_cache[cache_id] = {
            "name": room.name,
            "capacity": room.capacity,
            "type": room.type,
            "address": [
                site.address1,
                site.address2,
                site.address3,
                site.address4
            ],
            "site_name": site.sitename,
            "coordinates": {
                "lat": lat,
                "lng": lng
            }
        }

    return _rooms_cache[cache_id]


def get_student_timetable(upi, date_filter=None):
    r = redis.StrictRedis(
        host=settings.REDIS_UCLAPI_HOST,
        charset="utf-8",
        decode_responses=True
    )
    timetable_key = "timetable:personal:{}".format(upi)
    if r.exists(timetable_key):
        data = r.get(timetable_key)
        student_events = json.loads(data)
    else:
        student = _get_student_by_upi(upi)
        student_modules = _get_student_modules(student)
        student_events = _get_timetable_events(student_modules, True)
        # Celery task to cache for the next request
        cache_student_timetable.delay(upi, student_events)

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
