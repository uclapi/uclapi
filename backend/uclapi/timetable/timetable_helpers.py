import datetime

from django.conf import settings

from .models import Lock, StudentsA, StudentsB, \
    Stumodules, TimetableA, TimetableB, \
    WeekmapnumericA, WeekmapnumericB, \
    WeekstructureA, WeekstructureB

_SETID = settings.ROOMBOOKINGS_SETID

_week_map = {}
_week_num_date_map = {}


def _get_cache(model_name):
    models = {
        "students": [StudentsA, StudentsB],
        "timetable": [TimetableA, TimetableB],
        "weekmapnumeric": [WeekmapnumericA, WeekmapnumericB],
        "weekstructure": [WeekstructureA, WeekstructureB]
    }
    lock = Lock.objects.all()[0]
    model = models[model_name][0] if lock.a else models[model_name][1]
    return model


def _get_student_by_upi(upi):
    students = _get_cache("students")
    # Assume the current Set ID due to caching
    upi_upper = upi.upper()
    student = students.objects.filter(
        qtype2=upi_upper
    )
    return student


def _get_student_modules(student):
    student_modules = Stumodules.objects.filter(
        studentid=student.studentid,
        setid=_SETID
    )
    return student_modules


def _get_timetable_events(student_modules):
    if not _week_map:
        _map_weeks()

    timetable = _get_cache("timetable")
    student_timetable = []
    for module in student_modules:
        events_data = timetable.objects.filter(
            moduleid=module.moduleid,
            modgrpcode=module.modgrpcode
        )
        events = []
        for event in events_data:
            for date in _get_real_dates(event["slotid"]):
                events += {
                    "starttime": event["starttime"],
                    "endtime": event["finishtime"],
                    "duration": event["duration"],
                    "lecturerid": event["lecturerid"],
                    "moduletype": event["moduletype"],
                    "modgrpcode": event["modgrpcode"],
                    "siteid": event["siteid"],
                    "roomid": event["roomid"],
                    "startdate": date,
                    "moduleid": event["moduleid"],
                    "modulegroup": module["modgrpcode"]
                }
        student_timetable += events
    return student_modules


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


def get_student_timetable(upi):
    student = _get_student_by_upi(upi)
    student_modules = _get_student_modules(student)
    student_events = _get_timetable_events(student_modules)
    return student_events
