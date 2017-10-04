from django.shortcuts import render
from roombookings.helpers import PrettyJsonResponse as JsonResponse
from oauth.models import OAuthToken
from django.core.exceptions import ObjectDoesNotExist
from .models import Students, Course
from django.conf import settings
from .app_helpers import get_timetable, get_modules, get_course_modules
from rest_framework.decorators import api_view
from oauth.decorators import oauth_token_check

_SETID = settings.ROOMBOOKINGS_SETID


@api_view(["GET"])
@oauth_token_check(["timetable"])
def get_personal_timetable(request):
    try:
        token = request.GET["token"]
    except KeyError:
        return JsonResponse({
            "ok": False,
            "error": "No Oauth token found."
        })

    try:
        oauth_token = OAuthToken.objects.get(token=token)
        user = oauth_token.user
    except ObjectDoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "OAuth token doesn't exist."
        })

    try:
        student = Students.objects.filter(
            qtype2=user.employeeid, setid=settings.ROOMBOOKINGS_SETID)[0]
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
def get_modules_timetable(request):
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
def get_courses(request):
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
def get_modules(request):
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
        "modules": get_course_modules(courseid)
    })
