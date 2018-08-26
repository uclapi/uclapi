from django.conf import settings

from rest_framework.decorators import api_view

from common.helpers import PrettyJsonResponse as JsonResponse

from .models import Lock, Course, Depts, ModuleA, ModuleB

from .app_helpers import (
    get_custom_timetable,
    get_student_timetable, 
    get_departmental_modules
)

from common.decorators import uclapi_protected_endpoint

_SETID = settings.ROOMBOOKINGS_SETID


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=True, required_scopes=['timetable'])
def get_personal_timetable(request, *args, **kwargs):
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
    return JsonResponse(response, rate_limiting_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint()
def get_modules_timetable(request, *args, **kwargs):
    module_ids = request.GET.get("modules")
    if module_ids is None:
        return JsonResponse({
            "ok": False,
            "error": "No module IDs provided."
        }, rate_limiting_data=kwargs)

    try:
        modules = module_ids.split(',')
    except ValueError:
        return JsonResponse({
            "ok": False,
            "error": "Invalid module IDs provided."
        }, rate_limiting_data=kwargs)

    try:
        date_filter = request.GET["date_filter"]
        custom_timetable = get_custom_timetable(modules, date_filter)
    except KeyError:
        custom_timetable = get_custom_timetable(modules)

    if custom_timetable:
        response_json = {
            "ok": True,
            "timetable": custom_timetable
        }
        return JsonResponse(response_json, rate_limiting_data=kwargs)
    else:
        response_json = {
            "ok": False,
            "error": "One or more invalid Module IDs supplied."
        }
        response = JsonResponse(response_json, rate_limiting_data=kwargs)
        response.status_code = 400
        return response


@api_view(["GET"])
@uclapi_protected_endpoint()
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
    return JsonResponse(depts, rate_limiting_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint()
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
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    courses = {"ok": True, "courses": []}
    for course in Course.objects.filter(owner=department_id, setid=_SETID):
        courses["courses"].append({
            "course_name": course.name,
            "course_id": course.courseid,
            "years": course.numyears
        })
    return JsonResponse(courses, rate_limiting_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint()
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
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    modules = {
        "ok": True,
        "modules": get_departmental_modules(department_id)
    }

    return JsonResponse(modules, rate_limiting_data=kwargs)
