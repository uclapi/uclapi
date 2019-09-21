import json
import os
from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import quote
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from oauth.scoping import Scopes
from uclapi.settings import FAIR_USE_POLICY

from .app_helpers import get_temp_token, get_articles
from .models import App, User
from .tasks import add_user_to_mailing_list_task


@csrf_exempt
def shibboleth_callback(request):
    # should auth user login or signup
    # then redirect to dashboard homepage

    # Sometimes UCL doesn't give us the expected headers.
    # If a critical header is missing we error out.
    # If non-critical headers are missing we simply put a placeholder string.
    try:
        # This is used to find the correct user
        eppn = request.META['HTTP_EPPN']
        # We don't really use cn but because it's unique in the DB we can't
        # really put a place holder value.
        cn = request.META['HTTP_CN']
        # (aka UPI), also unique in the DB
        employee_id = request.META['HTTP_EMPLOYEEID']
    except KeyError:
        response = HttpResponse(
            (

                "Error 400 - Bad Request. <br>"
                "UCL has sent incomplete headers. If the issues persist please"
                "contact the UCL API Team to rectify this."
            )
        )
        response.status_code = 400
        return response

    # TODO: Ask UCL what on earth are they doing by missing out headers, and
    # remind them we need to to be informed of these types of changes.
    # TODO: log to sentry that fields were missing...
    department = request.META.get('HTTP_DEPARTMENT', '')
    given_name = request.META.get('HTTP_GIVENNAME', '')
    display_name = request.META.get('HTTP_DISPLAYNAME', '')
    groups = request.META.get('HTTP_UCLINTRANETGROUPS', '')

    # We first check whether the user is a member of any UCL Intranet Groups.
    # This is a quick litmus test to determine whether they should have
    # access to the dashboard.
    # We deny access to test accounts and alumni, neither of which have
    # this Shibboleth attribute.
    if not groups:
        response = HttpResponse(
            (
                "Error 403 - denied. <br>"
                "The API Dashboard is only assessible to active UCL users."
            )
        )
        response.status_code = 403
        return response

    try:
        # TODO: Handle MultipleObjectsReturned exception.
        # email field isn't unique at database level (on our side).
        # Alternatively, switch to employee_id (which is unique).
        user = User.objects.get(email=eppn)
    except ObjectDoesNotExist:
        # create a new user
        new_user = User(
            email=eppn,
            full_name=display_name,
            given_name=given_name,
            department=department,
            cn=cn,
            raw_intranet_groups=groups,
            employee_id=employee_id
        )

        new_user.save()
        add_user_to_mailing_list_task.delay(new_user.email, new_user.full_name)

        request.session["user_id"] = new_user.id
    else:
        # User exists already, so update the values if new ones are non-empty.
        request.session["user_id"] = user.id
        user.employee_id = employee_id
        if display_name:
            user.full_name = display_name
        if given_name:
            user.given_name = given_name
        if department:
            user.department = department
        if groups:
            user.raw_intranet_groups = groups
        user.save()

    return redirect(dashboard)


@ensure_csrf_cookie
def dashboard(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        url = os.environ["SHIBBOLETH_ROOT"] + "/Login?target="
        param = (request.build_absolute_uri(request.path) +
                 "user/login.callback")
        param = quote(param)
        url = url + param
        return redirect(url)

    user = User.objects.get(id=user_id)

    if not user.agreement:
        if request.method != "POST":
            return render(request, "Agreement.html", {
                'fair_use': FAIR_USE_POLICY
                })

        try:
            agreement = strtobool(request.POST["agreement"])
        except (KeyError, ValueError):
            return render(request, "Agreement.html", {
                'fair_use': FAIR_USE_POLICY,
                "error": "You must agree to the fair use policy"
            })

        if agreement:
            user.agreement = True
            user.save()
        else:
            return render(request, "Agreement.html", {
                'fair_use': FAIR_USE_POLICY,
                "error": "You must agree to the fair use policy"
            })

    user_meta = {
        "name": user.full_name,
        "cn": user.cn,
        "department": user.department,
        "intranet_groups": user.raw_intranet_groups,
        "apps": []
    }

    user_apps = App.objects.filter(user=user, deleted=False)

    s = Scopes()

    for app in user_apps:
        user_meta["apps"].append({
            "name": app.name,
            "id": app.id,
            "token": app.api_token,
            "created": app.created,
            "updated": app.last_updated,
            "oauth": {
                "client_id": app.client_id,
                "client_secret": app.client_secret,
                "callback_url": app.callback_url,
                "scopes": s.scope_dict_all(app.scope.scope_number)
            },
            "webhook": {
                "verification_secret": app.webhook.verification_secret,
                "url": app.webhook.url,
                "siteid": app.webhook.siteid,
                "roomid": app.webhook.roomid,
                "contact": app.webhook.contact
            }
        })

    initial_data = json.dumps(user_meta, cls=DjangoJSONEncoder)
    return render(request, 'Dashboard.html', {
        'initial_data': initial_data
    })

@ensure_csrf_cookie
def about(request):
    return render(request, 'AboutPage.html', {
        'initial_data': {}
    })

@ensure_csrf_cookie
def home(request):
    logged_in = True

    try:
        request.session["user_id"]
    except KeyError:
        logged_in = False

    articles = get_articles()
    token = get_temp_token()

    return render(request, 'HomePage.html', {
        'initial_data': {
            'temp_token': token,
            'logged_in': str(logged_in),
            'medium_articles': articles
        }
    })


@ensure_csrf_cookie
def documentation(request):
    return render(request, 'Documentation.html')
