import datetime
import json
from distutils.util import strtobool

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

from .amp import ModuleInstance
from .models import (DeptsA, DeptsB, LecturerA, LecturerB, Lock, ModuleA,
                     ModuleB, RoomsA, RoomsB, SitesA, SitesB, StudentsA,
                     StudentsB, StumodulesA, StumodulesB,  TimetableA,
                     TimetableB, WeekmapnumericA, WeekmapnumericB,
                     WeekstructureA, WeekstructureB,
                     CminstancesA, CminstancesB,
                     CourseA, CourseB,
                     CrscompmodulesA, CrscompmodulesB,
                     CrsavailmodulesA, CrsavailmodulesB)
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
_site_coord_cache = {}
_room_coord_cache = {}
_instance_cache = {}
_lecturers_cache = {}
_department_name_cache = {}


def get_cache(model_name):
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
        "departments": [DeptsA, DeptsB],
        "stumodules": [StumodulesA, StumodulesB],
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
        roombooking_lock = RBLock.objects.all()[0]
        if roombooking_lock.bookingA:
            model = roombookings_models[model_name][0]
        else:
            model = roombookings_models[model_name][1]
    else:
        raise Exception("Unknown model requested from cache")

    return model


def get_student_by_upi(upi):
    """Returns a StudentA or StudentB object by UPI"""
    students = get_cache("students")
    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )[0]
    return student


def _get_student_modules(student):
    """Returns all Stumodules object by for a given student"""
    stumodules = get_cache("stumodules")
    student_modules = stumodules.objects.filter(studentid=student.studentid)
    return student_modules


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
        return details

    details["name"] = lecturer.name
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

def _is_instance_in_criteria(instance, criteria):
    """Given (validated) criteria, determines if an instance meets it"""
    if criteria.get('term_1'):
        if strtobool(criteria.get('term_1')) != instance['periods']['teaching_periods']['term_1']:
            return False
    if criteria.get('term_2'):
        if strtobool(criteria.get('term_2')) != instance['periods']['teaching_periods']['term_2']:
            return False
    if criteria.get('term_3'):
        if strtobool(criteria.get('term_3')) != instance['periods']['teaching_periods']['term_3']:
            return False
    if criteria.get('term_1_next_year'):
        if strtobool(criteria.get('term_1_next_year')) != instance['periods']['teaching_periods']['term_1_next_year']:
            return False
    if criteria.get('summer'):
        if strtobool(criteria.get('summer')) != instance['periods']['teaching_periods']['summer']:
            return False
    if criteria.get('summer_school'):
        if strtobool(criteria.get('is_summer_school')) != instance['periods']['summer_school']['is_summer_school']:
            return False
    if criteria.get('summer_school_1'):
        if strtobool(criteria.get('summer_school_1')) != instance['periods']['summer_school']['sessions']['session_1']:
            return False
    if criteria.get('summer_school_2'):
        if strtobool(criteria.get('summer_school_2')) != instance['periods']['summer_school']['sessions']['session_2']:
            return False
    if criteria.get('lsr'):
        if strtobool(criteria.get('lsr')) != instance['periods']['lsr']:
            return False
    if criteria.get('year_long'):
        if strtobool(criteria.get('year_long')) != instance['periods']['year_long']:
            return False
    if criteria.get('is_undergraduate'):
        if strtobool(criteria.get('is_undergraduate')) != instance['delivery']['is_undergraduate']:
            return False
    if criteria.get('fheq_level'):
        if not criteria.get('fheq_level') == str(instance['delivery']['fheq_level']):
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
        'summer', 'summer_school', 'summer_school_1', 
        'summer_school_2', 'lsr', 'year_long', 'is_undergraduate'
    ] 
    valid_bools = ['1','0','true','false']
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

def _get_timetable_events(full_modules, stumodules):
    """
    Gets a dictionary of timetabled events.
    If stumodules=True then assume full_modules = [Stumodules]
    If stumodules=False then assume full_modules [ModuleA] or [ModuleB]
    """
    if not _week_map:
        _map_weeks()

    timetable = get_cache("timetable")
    modules = get_cache("module")

    bookings = get_cache("booking")
    event_bookings_list = {}
    full_timetable = {}
    modules_chosen = {}
    for module in full_modules:
        key = str(module.moduleid)+" "+str(module.instid)
        lab_key = key+str(module.modgrpcode)
        if key in modules_chosen:
            del modules_chosen[key]
        modules_chosen[lab_key] = module

    for _, module in modules_chosen.items():
        if stumodules:
            # Get events for the lab group assigned
            # Also include general lecture events (via the or operator)
            events_data = timetable.objects.filter(
                Q(modgrpcode=module.modgrpcode) | Q(modgrpcode='') | Q(modgrpcode=None),  # noqa
                moduleid=module.moduleid,
                instid=module.instid
            )
            module_data = modules.objects.get(
                moduleid=module.moduleid,
                instid=module.instid
            )
        else:
            events_data = timetable.objects.filter(
                moduleid=module.moduleid,
                instid=module.instid
            )
            module_data = module
        instance_data = _get_instance_details(module.instid)
        for event in events_data:
            if event.slotid not in event_bookings_list:
                event_bookings_list[event.slotid] =  \
                    bookings.objects.filter(slotid=event.slotid)
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
                        "contact": "Unknown",
                        "instance": instance_data
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

    return _get_timetable_events(full_modules, False)


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
    if session_type in _session_type_map:
        return _session_type_map[session_type]
    else:
        return "Unknown"


def _get_location_coordinates(siteid, roomid):
    # First try and get the specific room's location
    try:
        if roomid in _room_coord_cache:
            return _room_coord_cache[roomid]
        location = Location.objects.get(
            siteid=siteid,
            roomid=roomid
        )
        _room_coord_cache[roomid] = (location.lat, location.lng)
        return location.lat, location.lng
    except Location.DoesNotExist:
        pass

    # Now try and get the building's location
    try:
        if siteid in _site_coord_cache:
            return _site_coord_cache[siteid]
        location = SiteLocation.objects.get(
            siteid=siteid
        )
        _site_coord_cache[siteid] = (location.lat, location.lng)
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
        rooms = get_cache("rooms")
        sites = get_cache("sites")
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
        student = get_student_by_upi(upi)
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
    modules = get_cache("crscompmodules")
    for compulsory in modules.objects.filter(courseid=course_id, setid=_SETID).only('moduleid'):
        for module in get_cache("module").objects.filter(moduleid=compulsory.moduleid, setid=_SETID):
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
        modules = get_cache("crsavailmodules")
        for available in modules.objects.filter(courseid=course_id, setid=_SETID).only('moduleid'):
            for module in get_cache("module").objects.filter(moduleid=available.moduleid, setid=_SETID):
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
    dept_modules = {}
    if not query_params.get('only_available') == None:
        if strtobool(query_params.get('only_available')):
            _get_available_course_modules(dept_modules, course_id, query_params)
            return dept_modules

    if not query_params.get('only_compulsory') == None:
        if strtobool(query_params.get('only_compulsory')):
            _get_compulsory_course_modules(dept_modules, course_id, query_params)
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
