from django.shortcuts import render, redirect
from .models import User, App
from django.core.exceptions import ObjectDoesNotExist
import os
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.http import quote

from django.core.serializers.json import DjangoJSONEncoder
import json


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
    except KeyError as e:
        context = {
            "error": "Didn't receive all required Shibboleth data."
        }
        print(e)
        return render(
            request,
            'shibboleth_error.html',
            context=context,
            status=400
        )

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
    else:
        request.session["user_id"] = user.id

    return redirect(dashboard)

def index(request):

    if "user_id" in request.session:
        # user signed in

        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)

        user_meta = {
            "name": user.given_name,
            "cn": user.cn,
            "department": user.department,
            "intranet_groups": user.raw_intranet_groups,
            "apps": []
        }

        user_apps = App.objects.filter(user=user)

        for app in user_apps:
            user_meta["apps"].append({
                "name": app.name,
                "api_token": app.api_token,
                "created": app.created
            })
        return render(request, 'index.html', context=user_meta)
    else:
        # User not signed in
        # Build a sign in URL in the following format: SHIBBOLETH_ROOT + /Login?target=
        # + urlencode(full URI(current URL) + /user/login.callback)
        # This might look like the following:
        # - SHIBBOLETH_ROOT: https://uclapi.com/Shibboleth.sso
        # - /Login?target=
        # - quote (basically a url encode, but this is Python not PHP according to
        #       http://stackoverflow.com/a/7774038/5297057)
        # -- full URI
        # --- /dashboard
        # -- /user/login.callback
        # Result (example):
        # https://uclapi.com/Shibboleth.sso/Login?target=https%3A%2F%2Fuclapi.com%2Fdashboard%2Fuser%2Flogin.callback
        url = os.environ["SHIBBOLETH_ROOT"] + "/?target="
        param = request.build_absolute_uri(request.path) + "user/login.callback"
        param = quote(param)
        url = url + param
        return redirect(url)

@ensure_csrf_cookie
def dashboard(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        url = os.environ["SHIBBOLETH_ROOT"] + "/?target="
        param = request.build_absolute_uri(request.path) + "user/login.callback"
        param = quote(param)
        url = url + param
        return redirect(url)

    user = User.objects.get(id=user_id)

    user_meta = {
        "name": user.given_name,
        "cn": user.cn,
        "department": user.department,
        "intranet_groups": user.raw_intranet_groups,
        "apps": []
    }

    user_apps = App.objects.filter(user=user)

    for app in user_apps:
        user_meta["apps"].append({
            "name": app.name,
            "id": app.id,
            "token": app.api_token,
            "created": app.created,
            "updated": app.last_updated
        })

    initial_data = json.dumps(user_meta, cls=DjangoJSONEncoder)
    return render(request, 'dashboard.html', {
	'initial_data': initial_data
    }) 
