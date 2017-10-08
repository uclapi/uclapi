from django.conf import settings

from oauth.decorators import oauth_token_check

from rest_framework.decorators import api_view

from roombookings.helpers import PrettyJsonResponse as JsonResponse

from .models import StudentsA, StudentsB, Lock, Course, Depts, \
    ModuleA, ModuleB

from .app_helpers import get_timetable, get_modules, get_all_course_modules

from .timetable_helpers import get_student_timetable

_SETID = settings.ROOMBOOKINGS_SETID


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_personal_timetable(request, *args, **kwargs):
    token = kwargs['token']
    user = token.user

    # CMIS stores data as per an upper case representation of the UPI
    upi = user.employee_id.upper()

    # Get student information from cache
    lock = Lock.objects.all()[0]
    s = StudentsA if lock.a else StudentsB

    try:
        student = s.objects.filter(
            qtype2=upi, setid=_SETID)[0]
    except IndexError:
        return JsonResponse({
            "ok": False,
            "error": "Student does not have any assigned timetables."
        })

    return JsonResponse({
        "ok": True,
        "timetable": get_timetable(student)
    })


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_modules_timetable(request, *args, **kwargs):
    """
    Only get request accepted.
    Given a list of modulesids, this will return a yearly calendar for those
    courses.
    """
    module_ids = request.GET.get("modules")
    if module_ids is None:
        return JsonResponse({
            "ok": False,
            "error": "No module IDs provided."
        })

    try:
        modules = module_ids.split(',')
    except ValueError:
        return JsonResponse({
            "ok": False,
            "error": "Invalid module IDs provided."
        })

    return JsonResponse({
        "ok": True,
        "timetable": get_modules(modules)
    })


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_personal_timetable_fast(request, *args, **kwargs):
    token = kwargs['token']
    user = token.user
    try:
        date_filter = request.GET["date_filter"]
        timetable = get_student_timetable(user.employee_id, date_filter)
    except KeyError:
        timetable = get_student_timetable(user.employee_id)

    response = {
        "ok": True,
        "timetable": timetable
    }
    return JsonResponse(response)


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_departments(request, *args, **kwargs):
    """
    Returns all departments at UCL
    """
    depts = {"ok": True, "departments": []}
    for dept in Depts.objects.all():
        depts["departments"].append({
            "department_id": dept.deptid,
            "name": dept.name
        })
    return JsonResponse(depts)


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_department_courses(request, *args, **kwargs):
    """
    Returns all the courses in UCL with relevant ID
    """
    try:
        department_id = request.GET["department"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Supply a Department ID using the department parameter."
        })
        response.status_code = 200
        return response

    courses = {"ok": True, "courses": []}
    for course in Course.objects.filter(owner=department_id, setid=_SETID):
        courses["courses"].append({
            "course_name": course.name,
            "course_id": course.courseid,
            "years": course.numyears
        })
    return JsonResponse(courses)


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_department_modules(request, *args, **kwargs):
    """
    Returns all modules taught by a particular department.
    """
    try:
        department_id = request.GET["department"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Supply a Department ID using the department parameter."
        })
        response.status_code = 200
        return response

    modules = {"ok": True, "modules": []}
    lock = Lock.objects.all()[0]
    m = ModuleA if lock.a else ModuleB
    for module in m.objects.filter(owner=department_id, setid=_SETID):
        modules["modules"].append({
            "module_id": module.moduleid,
            "name": module.name,
            "module_code": module.linkcode,
            "class_size": module.csize
        })

    return JsonResponse(modules)


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_course_modules(request, *args, **kwargs):
    """
    Returns all the modules in the specified course.
    @param: courseid
    """
    courseid = request.GET.get("courseid")
    if not courseid:
        return JsonResponse({
            "ok": False,
            "error": "No courseid found."
        })

    return JsonResponse({
        "ok": True,
        "modules": get_all_course_modules(courseid)
    })
