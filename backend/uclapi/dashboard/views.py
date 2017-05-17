from django.shortcuts import render, redirect
from .models import User, App
from django.core.exceptions import ObjectDoesNotExist
import os
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.http import quote
from distutils.util import strtobool
from uclapi.settings import FAIR_USE_POLICY

from django.core.serializers.json import DjangoJSONEncoder
import json
import keen


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
        keen.add_event("signup", {
            "id": new_user.id,
            "email": eppn,
            "name": display_name
        })
    else:
        request.session["user_id"] = user.id

    return redirect(dashboard)


@ensure_csrf_cookie
def dashboard(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        url = os.environ["SHIBBOLETH_ROOT"] + "/Login?target="
        param = request.build_absolute_uri(request.path) + "user/login.callback"
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
