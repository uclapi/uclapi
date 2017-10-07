from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from oauth.decorators import oauth_token_check
from oauth.models import OAuthToken

from rest_framework.decorators import api_view

from roombookings.helpers import PrettyJsonResponse as JsonResponse

from .models import Students, Course
from .app_helpers import get_timetable, get_modules, get_all_course_modules

_SETID = settings.ROOMBOOKINGS_SETID


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_personal_timetable(request, *args, **kwargs):
    token = kwargs['token']
    user = token.user

    # CMIS stores data as per an upper case representation of the UPI
    upi = user.employee_id.upper()

    try:
        student = Students.objects.filter(
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


@api_view(["POST"])
@oauth_token_check(["timetable"])
def get_modules_timetable(request, *args, **kwargs):
    """
    Only post request accepted.
    Given a list of modulesids, this will return a yearly calendar for those
    courses.
    """
    module_ids = request.POST.getlist("modules")
    if not module_ids:
        return JsonResponse({
            "ok": False,
            "error": "No module ids provided."
        })

    return JsonResponse({
        "ok": True,
        "timetable": get_modules(module_ids)
    })


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_courses(request, *args, **kwargs):
    """
    Returns all the courses in UCL with relevant ID
    """
    courses = {"ok": True, "courses": []}
    for course in Course.objects.all():
        courses["courses"].append({
            "course_name": course.name,
            "couse_id": course.courseid,
            "year": course.numyears
        })
    return JsonResponse(courses)


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
