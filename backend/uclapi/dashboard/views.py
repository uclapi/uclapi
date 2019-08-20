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
    # We first check whether the user is a member of any UCL Intranet Groups.
    # This is a quick litmus test to determine whether they should have
    # access to the dashboard.
    # We deny access to test accounts and alumni, neither of which have
    # this Shibboleth attribute.
    if 'HTTP_UCLINTRANETGROUPS' not in request.META:
        response = HttpResponse(
            (
                "Error 403 - denied. <br>"
                "The API Dashboard is only assessible to active UCL users."
            )
        )
        response.status_code = 403
        return response

    # should auth user login or signup
    # then redirect to dashboard homepage
    eppn = request.META['HTTP_EPPN']
    groups = request.META['HTTP_UCLINTRANETGROUPS']
    cn = request.META['HTTP_CN']
    department = request.META['HTTP_DEPARTMENT']
    given_name = request.META['HTTP_GIVENNAME']
    display_name = request.META['HTTP_DISPLAYNAME']
    employee_id = request.META['HTTP_EMPLOYEEID']

    try:
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
        # user exists already, update values
        request.session["user_id"] = user.id
        user.full_name = display_name
        user.given_name = given_name
        user.department = department
        user.raw_intranet_groups = groups
        user.employee_id = employee_id
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
            return render(request, "agreement.html", {
                'fair_use': FAIR_USE_POLICY
                })

        try:
            agreement = strtobool(request.POST["agreement"])
        except (KeyError, ValueError):
            return render(request, "agreement.html", {
                'fair_use': FAIR_USE_POLICY,
                "error": "You must agree to the fair use policy"
            })

        if agreement:
            user.agreement = True
            user.save()
        else:
            return render(request, "agreement.html", {
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
    return render(request, 'dashboard.html', {
        'initial_data': initial_data
    })


@ensure_csrf_cookie
def get_started(request):
    logged_in = True

    try:
        request.session["user_id"]
    except KeyError:
        logged_in = False

    articles = get_articles()
    token = get_temp_token()

    return render(request, 'getStarted.html', {
        'initial_data': {
            'temp_token': token,
            'logged_in': str(logged_in),
            'medium_articles': articles
        }
    })


@ensure_csrf_cookie
def documentation(request):
    return render(request, 'documentation.html')
