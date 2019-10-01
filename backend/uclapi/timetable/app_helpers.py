import datetime
import json
from distutils.util import strtobool

import redis
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from roombookings.models import (
    BookingA,
    BookingB,
    RoomA,
    RoomB
)

from .amp import ModuleInstance
from .models import (
    CminstancesA, CminstancesB,
    CourseA, CourseB,
    CrscompmodulesA, CrscompmodulesB,
    CrsavailmodulesA, CrsavailmodulesB,
    DeptsA, DeptsB,
    LecturerA, LecturerB,
    Lock,
    ModuleA, ModuleB,
    SitesA, SitesB,
    StudentsA, StudentsB,
    TimetableA, TimetableB,
    WeekmapnumericA, WeekmapnumericB,
    WeekstructureA, WeekstructureB
)
from .personal_timetable import get_personal_timetable
from .tasks import cache_student_timetable
from .utils import (
    get_location_coordinates,
    SESSION_TYPE_MAP
)

_SETID = settings.ROOMBOOKINGS_SETID

_week_map = {}
_week_num_date_map = {}
_rooms_cache = {}
_instance_cache = {}
_department_name_cache = {}
_lecturers_cache = {}
_lecturers_cache[None] = {
    "name": "Unknown",
    "email": "Unknown",
    "department_id": "Unknown",
    "department_name": "Unknown"
}


def get_cache(model_name):
    """Returns the cache bucket for the requested model name"""
    timetable_models = {
        "module": [ModuleA, ModuleB],
        "students": [StudentsA, StudentsB],
        "timetable": [TimetableA, TimetableB],
        "weekmapnumeric": [WeekmapnumericA, WeekmapnumericB],
        "weekstructure": [WeekstructureA, WeekstructureB],
        "lecturer": [LecturerA, LecturerB],
        "rooms": [RoomA, RoomB],
        "sites": [SitesA, SitesB],
        "departments": [DeptsA, DeptsB],
        "cminstances": [CminstancesA, CminstancesB],
        "course": [CourseA, CourseB],
        "crsavailmodules": [CrsavailmodulesA, CrsavailmodulesB],
        "crscompmodules": [CrscompmodulesA, CrscompmodulesB]
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
        roombooking_lock = Lock.objects.all()[0]
        if roombooking_lock.a:
            model = roombookings_models[model_name][0]
        else:
            model = roombookings_models[model_name][1]
    else:
        raise Exception("Unknown model requested from cache")

    return model


def _get_full_department_name(department_code):
    """Converts a department code, such as COMPS_ENG, into a full name
    such as Computer Science"""
    if department_code in _department_name_cache:
        return _department_name_cache[department_code]
    else:
        departments = get_cache("departments")
        try:
            dept = departments.objects.get(deptid=department_code)
            _department_name_cache[department_code] = dept.name
            return dept.name
        except ObjectDoesNotExist:
            return "Unknown"


def _get_lecturer_details(lecturer_upi):
    """Returns a lecturer's name and email address from their UPI"""
    if lecturer_upi in _lecturers_cache:
        return _lecturers_cache[lecturer_upi]
    lecturers = get_cache("lecturer")
    details = {
        "name": "Unknown",
        "email": "Unknown",
        "department_id": "Unknown",
        "department_name": "Unknown"
    }
    try:
        lecturer = lecturers.objects.get(lecturerid=lecturer_upi)
    except ObjectDoesNotExist:
        _lecturers_cache[lecturer_upi] = details
        return details

    details["name"] = lecturer.name
    if lecturer.linkcode:
        details["email"] = lecturer.linkcode + "@ucl.ac.uk"

    if lecturer.owner:
        details["department_id"] = lecturer.owner
        details["department_name"] = _get_full_department_name(lecturer.owner)
    _lecturers_cache[lecturer_upi] = details
    return details


def _get_instance_details(instid):
    if instid in _instance_cache:
        return _instance_cache[instid]
    cminstances = get_cache("cminstances")
    instance_data = cminstances.objects.get(instid=instid)
    instance = ModuleInstance(instance_data.instcode)
    data = {
        "delivery": instance.delivery.get_delivery(),
        "periods": instance.periods.get_periods(),
        "instance_code": instance_data.instcode
    }
    _instance_cache[instid] = data
    return data


def _is_instance_in_criteria(instance, query_params):
    """
    Given (validated) criteria, determines if an instance meets it

    :param instance: instance details
    :type instance: dict
    :param query_params: parameters given by the user to the endpoint
    :type query_params: django.http.QueryDict

    :returns: True if instance is in criteria (query_params)
    :rtype: bool
    """
    criteria_list = [
        'term_1',
        'term_2',
        'term_3',
        'term_1_next_year',
        'summer',
        'is_summer_school',
        'session_1',
        'session_2',
        'lsr',
        'year_long',
        'is_undergraduate',
        'fheq_level'
    ]
    comparator = {}
    for i in range(len(criteria_list)):
        if query_params.get(criteria_list[i]):
            if i < 5:
                comparator = instance['periods']['teaching_periods']
            elif i < 6:
                comparator = instance['periods']['summer_school']
            elif i < 8:
                comparator = instance['periods']['summer_school']['sessions']
            elif i < 10:
                comparator = instance['periods']
            elif i < 11:
                comparator = instance['delivery']
            else:
                comparator = instance['delivery']
                if (comparator[criteria_list[i]] !=
                        int(query_params.get(criteria_list[i]))):
                    return False
                continue
            if (comparator[criteria_list[i]] !=
                    strtobool(query_params.get(criteria_list[i]))):
                return False
    return True


def validate_amp_query_params(query_params):
    """
    Validates that query params concerning AMP are of the valid type

    :param query_params: parameters given by the user to the endpoint
    :type query_params: django.http.QueryDict

    :returns: True if query parameters are of valid form, False otherwise
    :rtype: bool
    """
    bool_params = [
        'term_1', 'term_2', 'term_3', 'term_1_next_year',
        'summer', 'is_summer_school', 'session_1',
        'session_2', 'lsr', 'year_long', 'is_undergraduate'
    ]

    for param in bool_params:
        if query_params.get(param):
            try:
                strtobool(query_params.get(param))
            except ValueError:
                return False
    if query_params.get('fheq_level'):
        try:
            int(query_params.get('fheq_level'))
        except ValueError:
            return False
    return True


def _get_timetable_events(full_modules):
    """
    Gets a dictionary of timetabled events for a list of Module objects
    """
    if not _week_map:
        _map_weeks()

    timetable = get_cache("timetable")

    bookings = get_cache("booking")
    distinct_fields = (
        'setid', 'siteid', 'roomid', 'sitename', 'roomname', 'bookabletype',
        'slotid', 'bookingid', 'starttime', 'finishtime', 'startdatetime',
        'finishdatetime', 'weeknumber', 'condisplayname', 'phone', 'descrip',
    )
    event_bookings_list = {}
    full_timetable = {}
    modules_chosen = {}
    for module in full_modules:
        key = str(module.moduleid) + " " + str(module.instid)
        try:
            lab_key = key + str(module.modgrpcode)
        except AttributeError:
            lab_key = key
        if key in modules_chosen:
            del modules_chosen[key]
        modules_chosen[lab_key] = module

    for _, module in modules_chosen.items():
        events_data = timetable.objects.filter(
            moduleid=module.moduleid,
            instid=module.instid
        )
        instance_data = _get_instance_details(module.instid)
        for event in events_data:
            if event.slotid not in event_bookings_list:
                event_bookings_list[event.slotid] =  \
                        bookings.objects \
                                .filter(
                                    slotid=event.slotid,
                                ).distinct(*distinct_fields)
            event_bookings = event_bookings_list[event.slotid]
            # .exists() instead of len so we don't evaluate all of the filter
            if not event_bookings.exists():
                # We have to trust the data in the event because
                # no rooms are booked for some weird reason.
                for date in _get_real_dates(event):
                    event_data = {
                        "start_time": event.starttime,
                        "end_time": event.finishtime,
                        "duration": event.duration,
                        "module": {
                            "module_id": module.moduleid,
                            "department_id": event.owner,
                            "department_name": _get_full_department_name(
                                event.owner
                            ),
                            "name": module.name
                        },
                        "location": _get_location_details(
                            event.siteid,
                            event.roomid
                        ),
                        "session_title": module.name,
                        "session_type": event.moduletype,
                        "session_type_str": _get_session_type_str(
                            event.moduletype
                        ),
                        "contact": "Unknown",
                        "instance": instance_data
                    }

                    # Check if the module timetable event's Lecturer ID
                    # exists. If not, we use the Lecturer ID associated
                    # with the module as a whole. If neither exist then
                    # we say that we don't know. It's an ugly hack, but
                    # it works around not all timetabled lectures having
                    # the Lecturer ID field filled as they should.
                    if event.lecturerid:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(event.lecturerid.strip())
                    elif module.lecturerid:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(module.lecturerid.strip())
                    else:
                        # This will give us 'Unknown' in all fields
                        event_data["module"]["lecturer"] = \
                            _lecturers_cache[None]

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
                            "module_id": module.moduleid,
                            "department_id": event.owner,
                            "department_name": _get_full_department_name(
                                event.owner
                            ),
                            "name": module.name
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
                        "contact": booking.condisplayname,
                        "instance": instance_data
                    }

                    # Check if the module timetable event's Lecturer ID
                    # exists. If not, we use the Lecturer ID associated
                    # with the module as a whole. If neither exist then
                    # we say that we don't know. It's an ugly hack, but
                    # it works around not all timetabled lectures having
                    # the Lecturer ID field filled as they should.
                    if event.lecturerid:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(event.lecturerid.strip())
                    elif module.lecturerid:
                        event_data["module"]["lecturer"] = \
                            _get_lecturer_details(module.lecturerid.strip())
                    else:
                        # This will give us 'Unknown' in all fields
                        event_data["module"]["lecturer"] = \
                            _lecturers_cache[None]

                    date_str = booking.startdatetime.strftime("%Y-%m-%d")
                    if date_str not in full_timetable:
                        full_timetable[date_str] = []
                    full_timetable[date_str].append(event_data)
    return full_timetable


def _get_timetable_events_module_list(module_list):
    if not _week_map:
        _map_weeks()

    modules = get_cache("module")
    cminstances = get_cache("cminstances")

    full_modules = []

    for module in module_list:
        try:
            if "-" in module and len(module) > 9:
                # An instance was requested, so filter by it
                hyphen_pos = module.index('-')
                instcode = module[hyphen_pos + 1:]
                instid = cminstances.objects.filter(
                    instcode=instcode
                )[0].instid
                full_modules.append(modules.objects.get(
                    moduleid=module[:hyphen_pos],
                    instid=instid
                ))
            else:
                for m in modules.objects.filter(moduleid=module):
                    full_modules.append(m)
            # full_modules.append(modules.objects.filter(moduleid=module))
        except (ObjectDoesNotExist, ValueError):
            return False

    return _get_timetable_events(full_modules)


def _map_weeks():
    weekmapnumeric = get_cache("weekmapnumeric")
    weekstructure = get_cache("weekstructure")
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
    if session_type in SESSION_TYPE_MAP:
        return SESSION_TYPE_MAP[session_type]
    else:
        return "Unknown"


def _get_location_details(siteid, roomid):
    if not roomid:
        return {}
    if not siteid:
        return {}

    cache_id = siteid + "___" + roomid
    if cache_id not in _rooms_cache:
        rooms = get_cache("rooms")
        sites = get_cache("sites")
        try:
            room = rooms.objects.filter(roomid=roomid, siteid=siteid)[0]
            site = sites.objects.filter(siteid=siteid)[0]
        except IndexError:
            return {}
        lat, lng = get_location_coordinates(siteid, roomid)
        _rooms_cache[cache_id] = {
            "name": room.roomname,
            "capacity": room.capacity,
            "type": room.bookabletype,
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
    r = redis.Redis(
        host=settings.REDIS_UCLAPI_HOST,
        charset="utf-8",
        decode_responses=True
    )
    timetable_key = "timetable:personal:{}".format(upi)
    if r.exists(timetable_key):
        data = r.get(timetable_key)
        student_events = json.loads(data)
    else:
        student_events = get_personal_timetable(upi)
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


def get_departmental_modules(department_id):
    modules = get_cache("module")
    dept_modules = {}
    for module in modules.objects.filter(owner=department_id, setid=_SETID):
        instance_data = _get_instance_details(module.instid)

        if module.moduleid not in dept_modules:
            dept_modules[module.moduleid] = {
                "module_id": module.moduleid,
                "name": module.name,
                "instances": []
            }

        dept_modules[module.moduleid]['instances'].append({
            "full_module_id": "{}-{}".format(
                module.moduleid,
                instance_data['instance_code']
            ),
            "class_size": module.csize,
            ** instance_data
        })

    return dept_modules


def _get_compulsory_course_modules(dept_modules, course_id, query_params):
    """
    Gets all compulsory modules on a given course,
    filtering by instance criteria.

    :param dept_modules: dictionary of department modules
    :type dept_modules: dict
    :param course_id: course id
    :type course_id: str
    :param query_params: dictionary of validated query parameters
    :type query_params: django.http.QueryDict

    """
    modules = get_cache("crscompmodules")
    for compulsory in modules.objects \
                             .filter(courseid=course_id, setid=_SETID) \
                             .only('moduleid'):
        for module in get_cache("module").objects \
                                         .filter(moduleid=compulsory.moduleid,
                                                 setid=_SETID):
            instance_data = _get_instance_details(module.instid)
            if not _is_instance_in_criteria(instance_data, query_params):
                continue

            if module.moduleid not in dept_modules:
                dept_modules[module.moduleid] = {
                    "module_id": module.moduleid,
                    "name": module.name,
                    "instances": []
                }

            dept_modules[module.moduleid]['instances'].append({
                "full_module_id": "{}-{}".format(
                    module.moduleid,
                    instance_data['instance_code']
                ),
                "class_size": module.csize,
                ** instance_data
            })


def _get_available_course_modules(dept_modules, course_id, query_params):
    """
    Gets all available modules on a given course,
    filtering by instance criteria.

    :param dept_modules: dictionary of department modules
    :type dept_modules: dict
    :param course_id: course id
    :type course_id: str
    :param query_params: dictionary of validated criteria
    :type query_params: django.http.QueryDict

    """
    modules = get_cache("crscompmodules")
    modules = get_cache("crsavailmodules")
    for available in modules.objects \
                            .filter(courseid=course_id, setid=_SETID) \
                            .only('moduleid'):
        for module in get_cache("module").objects \
                                            .filter(
                                                moduleid=available.moduleid,
                                                setid=_SETID
                                            ):
            instance_data = _get_instance_details(module.instid)
            if not _is_instance_in_criteria(instance_data, query_params):
                continue

            if module.moduleid not in dept_modules:
                dept_modules[module.moduleid] = {
                    "module_id": module.moduleid,
                    "name": module.name,
                    "instances": []
                }

            dept_modules[module.moduleid]['instances'].append({
                "full_module_id": "{}-{}".format(
                    module.moduleid,
                    instance_data['instance_code']
                ),
                "class_size": module.csize,
                ** instance_data
            })


def get_course_modules(course_id, query_params):
    """
    Gets all modules on a given course, filtering by instance criteria.

    :param course_id: course id
    :type course_id: str
    :param query_params: dictionary of validated criteria
    :type query_params: django.http.QueryDict

    :returns: course modules, filtered by instance criteria
    :rtype: dict

    """
    dept_modules = {}
    if not query_params.get('only_available') is None:
        if strtobool(query_params.get('only_available')):
            _get_available_course_modules(dept_modules,
                                          course_id,
                                          query_params)
            return dept_modules

    if not query_params.get('only_compulsory') is None:
        if strtobool(query_params.get('only_compulsory')):
            _get_compulsory_course_modules(dept_modules,
                                           course_id,
                                           query_params)
            return dept_modules

    _get_available_course_modules(dept_modules, course_id, query_params)
    _get_compulsory_course_modules(dept_modules, course_id, query_params)
    return dept_modules


def get_departments():
    depts = get_cache("departments")
    departments = []
    for dept in depts.objects.all():
        departments.append({
            "department_id": dept.deptid,
            "name": dept.name
        })
    return departments
