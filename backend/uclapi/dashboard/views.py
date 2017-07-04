import json
import os
from distutils.util import strtobool

from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render
from django.utils.http import quote
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from uclapi.settings import FAIR_USE_POLICY

from .models import App, User, TemporaryToken
from oauth.scoping import Scopes

from .tasks import keen_add_event_task as keen_add_event


@csrf_exempt
def shibboleth_callback(request):
    # this view is user facing, so should return html error page
    # should auth user login or signup
    # then redirect to dashboard homepage
    try:
        eppn = request.META['HTTP_EPPN']
        groups = request.META['HTTP_UCLINTRANETGROUPS']
        cn = request.META['HTTP_CN']
        department = request.META['HTTP_DEPARTMENT']
        given_name = request.META['HTTP_GIVENNAME']
        display_name = request.META['HTTP_DISPLAYNAME']
        employee_id = request.META['HTTP_EMPLOYEEID']
    except KeyError:
        # didn't receive all required data

        # Delete this code on September 26th 2017! Temporary shib workaround
        implied_eppn = "{}@ucl.ac.uk".format(cn)
        login_reminder = "login-after-2017-09-26-to-fix"
        try:
            user = User.objects.get(email=implied_eppn)
        except ObjectDoesNotExist:
            # create new user
            new_user = User(
                email=implied_eppn,
                full_name="temp-full-name-{}".format(login_reminder),
                given_name="temp-given-name-{}".format(login_reminder),
                department="temp-department-{}".format(login_reminder),
                cn=cn,
                raw_intranet_groups="temp-groups-{}".format(login_reminder),
                employee_id="temp-not-real-upi-{}".format(cn)
            )
            new_user.save()

            request.session["user_id"] = new_user.id
            keen_add_event.delay("signup", {
                "id": new_user.id,
                "email": eppn,
                "name": display_name
            })
        else:
            # user already exists, log them in
            request.session["user_id"] = user.id

        # end temporary shib workaround - delete until here

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
        request.session["user_id"] = new_user.id
        keen_add_event.delay("signup", {
            "id": new_user.id,
            "email": eppn,
            "name": display_name
        })
    else:
        # user exists already, update values
        request.session["user_id"] = user.id
        user.full_name = display_name
        user.given_name = given_name
        user.department = department
        user.raw_intranet_groups = groups
        user.employee_id = employee_id
        user.save()

        keen_add_event.delay("User data updated", {
            "id": user.id,
            "email": eppn,
            "name": display_name
        })

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

    temp_token = TemporaryToken.objects.create()
    return render(request, 'getStarted.html', {
        'initial_data': {
            'temp_token': temp_token.api_token,
            'logged_in': str(logged_in)
        }
    })
