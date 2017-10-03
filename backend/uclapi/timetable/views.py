from django.shortcuts import render
from roombookings.helpers import PrettyJsonResponse as JsonResponse
from dashboard.models import User
from oauth.models import OAuthToken
from django.core.exceptions import ObjectDoesNotExist
from .models import Students
from django.conf import settings
from .app_helpers import get_timetable


# Create your views here.
def get_personal_timetable(request):
    # try:
    #     token = request.GET["token"]
    # except KeyError:
    #     return JsonResponse({
    #         "ok": False,
    #         "error": "No Oauth token found."
    #     })
    #
    # try:
    #     oauth_token = OAuthToken.objects.get(token=token)
    #     user = oauth_token.user
    # except ObjectDoesNotExist:
    #     return JsonResponse({
    #         "ok": False,
    #         "error": "OAuth token doesn't exist."
    #     })

    try:
        student = Students.objects.filter(
            qtype2="AFPUN08", setid=settings.ROOMBOOKINGS_SETID)[0]
    except IndexError:
        return JsonResponse({
            "ok": False,
            "error": "Student does not have any assigned timetables."
        })

    return JsonResponse(get_timetable(student))
