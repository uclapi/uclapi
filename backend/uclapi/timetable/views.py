from django.conf import settings

from rest_framework.decorators import api_view

from common.helpers import PrettyJsonResponse as JsonResponse

from .models import Course

from .app_helpers import (
    get_custom_timetable,
    get_departmental_modules,
    get_departments,
    get_student_timetable,
    get_course_modules
)

from common.decorators import uclapi_protected_endpoint

_SETID = settings.ROOMBOOKINGS_SETID


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=True,
    required_scopes=['timetable'],
    last_modified_redis_key='timetable_gencache'
)
def get_personal_timetable_endpoint(request, *args, **kwargs):
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
    return JsonResponse(response, custom_header_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint(
    last_modified_redis_key='timetable_gencache'
)
def get_modules_timetable_endpoint(request, *args, **kwargs):
    module_ids = request.GET.get("modules")
    if module_ids is None:
        return JsonResponse({
            "ok": False,
            "error": "No module IDs provided."
        }, custom_header_data=kwargs)

    try:
        modules = module_ids.split(',')
    except ValueError:
        return JsonResponse({
            "ok": False,
            "error": "Invalid module IDs provided."
        }, custom_header_data=kwargs)

    date_filter = request.GET.get("date_filter")
    custom_timetable = get_custom_timetable(modules, date_filter)

    if custom_timetable:
        response_json = {
            "ok": True,
            "timetable": custom_timetable
        }
        return JsonResponse(response_json, custom_header_data=kwargs)
    else:
        response_json = {
            "ok": False,
            "error": "One or more invalid Module IDs supplied."
        }
        response = JsonResponse(response_json, custom_header_data=kwargs)
        response.status_code = 400
        return response


@api_view(["GET"])
@uclapi_protected_endpoint(
    last_modified_redis_key='timetable_gencache'
)
def get_departments_endpoint(request, *args, **kwargs):
    """
    Returns all departments at UCL
    """
    departments = {
        "ok": True,
        "departments": get_departments()
    }
    return JsonResponse(departments, custom_header_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint(
    last_modified_redis_key='timetable_gencache'
)
def get_department_courses_endpoint(request, *args, **kwargs):
    """
    Returns all the courses in UCL with relevant ID
    """
    try:
        department_id = request.GET["department"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Supply a Department ID using the department parameter."
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    courses = {"ok": True, "courses": []}
    for course in Course.objects.filter(owner=department_id, setid=_SETID, linkcode="YY"):
        courses["courses"].append({
            "course_name": course.name,
            "course_id": course.courseid,
            "years": course.numyears
        })
    return JsonResponse(courses, custom_header_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint(
    last_modified_redis_key='timetable_gencache'
)
def get_department_modules_endpoint(request, *args, **kwargs):
    """
    Returns all modules taught by a particular department.
    """
    try:
        department_id = request.GET["department"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Supply a Department ID using the department parameter."
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    modules = {
        "ok": True,
        "modules": get_departmental_modules(department_id)
    }

    return JsonResponse(modules, custom_header_data=kwargs)


@api_view(["GET"])
@uclapi_protected_endpoint(
    last_modified_redis_key='timetable_gencache'
)
def get_course_modules_endpoint(request, *args, **kwargs):
    """
    Returns all modules taught on a particular course.
    """
    try:
        course_id = request.GET["course"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Supply a Course ID using the department courses parameter."
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    bool_params = [
        'term_1', 'term_2', 'term_3', 'term_1_next_year',
        'summer', 'summer_school', 'summer_school_1', 
        'summer_school_2', 'lsr', 'year_long', 'is_undergraduate'
    ] 
    valid_bools = ['1','0','true','false']
    for param in bool_params:
        if request.query_params.get(param):
            if request.query_params.get(param) not in valid_bools:
                response = JsonResponse({
                    "ok": False,
                    "error": "The parameter '{}' must be given as a valid."
                             "boolean value (1,0,true,false)".format(param)
                }, custom_header_data=kwargs)
                response.status_code = 400
                return response
    if request.query_params.get('fheq_level'):
        try:
            int(request.query_params.get('fheq_level'))
        except ValueError:
            response = JsonResponse({
                "ok": False,
                "error": "Please supply the parameter 'fheq_level' as a valid integer."
            }, custom_header_data=kwargs)
            response.status_code = 400
            return response

    modules = {
        "ok": True,
        "modules": get_course_modules(course_id, request.query_params)
    }

    return JsonResponse(modules, custom_header_data=kwargs)
