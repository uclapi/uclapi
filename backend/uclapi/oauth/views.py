from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core import signing
from django.core.signing import TimestampSigner
from django.utils.http import quote
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect

from dashboard.models import App, User

import os
import json

# The endpoint that creates a Shibboleth login and redirects the user to it
def authorise(request):
    client_id = request.GET.get("client_id", None)
    state = request.GET.get("state", None)
    if not (client_id and state):
        return JsonResponse({
            "ok": False,
            "error": "incorrect parameters supplied"
        })
    
    try:
        app = App.objects.get(client_id=client_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "App does not exist for client id"
        })

    # Sign the app and state pair before heading to Shibboleth to help protect
    # against CSRF and XSS attacks
    signer = TimestampSigner()
    data = app.client_id + "|" + state
    signed_data = signer.sign(data)

    # Build Shibboleth callback URL
    url = os.environ.get("SHIBBOLETH_ROOT") + "/Login?target="
    target = request.build_absolute_uri(request.path)
    target += "shibcallback?appdata="
    target += signed_data
    target = quote(target)
    url += target

    # Send the user to Shibboleth to log in
    return redirect(url)

@csrf_exempt
@ensure_csrf_cookie
def shibcallback(request):
    # Callback from Shib login. Get ALL the meta!
    appdata_signed = request.GET.get("appdata", None)
    if not appdata_signed:
        return JsonResponse({
            "ok": False,
            "error": "No signed app data returned from Shibboleth. Please use the authorise endpoint."
        })

    signer = TimestampSigner()
    try:
        # Expire our signed tokens after five minutes for added security
        appdata = signer.unsign(appdata_signed, max_age=300)
    except signing.BadSignature:
        return JsonResponse({
            "ok": False,
            "error": "Bad signature. Please try login again."
        })
    except signing.SignatureExpired:
        return JsonResponse({
            "ok": False,
            "error": "Signature has expired. Please try login again."
        })
    
    parts = appdata.split("|")
    client_id = parts[0]
    state = parts[1]

    app = App.objects.get(client_id=client_id)

    try:
        eppn = request.META['HTTP_EPPN']
        groups = request.META['HTTP_UCLINTRANETGROUPS']
        cn = request.META['HTTP_CN']
        department = request.META['HTTP_DEPARTMENT']
        given_name = request.META['HTTP_GIVENNAME']
        display_name = request.META['HTTP_DISPLAYNAME']
        employee_id = request.META['HTTP_EMPLOYEEID']
    except:
        context = {
            "error": "Didn't receive all required Shibboleth data."
        }
        return render(
            request,
            'shibboleth_error.html',
            context=context,
            status=400
        )

    # If a user has never used the API before then we need to sign them up
    try:
        user = User.objects.get(email=eppn)
    except ObjectDoesNotExist:
        # create a new user
        user = User(
            email=eppn,
            full_name=display_name,
            given_name=given_name,
            department=department,
            cn=cn,
            raw_intranet_groups=groups,
            employee_id=employee_id
        )

        user.save()
        keen.add_event("signup", {
            "id": user.id,
            "email": eppn,
            "name": display_name
        })
    
    signer = TimestampSigner()
    response_data = {
        "client_id": app.client_id,
        "state": state,
        "user_upi": user.employee_id
    }

    response_data_str = json.dumps(response_data, cls=DjangoJSONEncoder)
    response_data_signed = signer.sign(response_data_str)

    page_data = {
        "app_name": app.name,
        "creator": app.user.full_name,
        "client_id": app.client_id,
        "state": state,
        "scope": {
            "private_roombookings": app.scope.private_roombookings,
            "private_timetable": app.scope.private_timetable,
            "private_uclu": app.scope.private_uclu
        },
        "user": {
            "full_name": user.full_name,
            "cn": user.cn,
            "email": user.email,
            "department": user.department,
            "upi": user.employee_id
        },
        "signed_data": response_data_signed
    }

    initial_data = json.dumps(page_data, cls=DjangoJSONEncoder)
    return render(request, 'permissions.html',
    {
        'initial_data': initial_data
    })


@csrf_protect
def userdeny(request):
    signer = TimestampSigner()

    try:
        signed_data = request.POST.get("signed_app_data")
        raw_data_str = signer.unsign(signed_data, max_age=300)
    except:
        return JsonResponse({
            "ok": False,
            "error": "The signed data received was invalid. Please try the login process again. If this issue persists, please contact support."
        })
    
    try:
        data = json.loads(raw_data_str)
    except:
        return JsonResponse({
            "ok": False,
            "error": "The JSON data was not in the expected format. Please contact support."
        })

    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    redir = app.callback_url + "?denied&state=" + state
    
    return redirect(redir)
    
@csrf_protect
def userallow(request):
    signer = TimestampSigner()

    try:
        raw_data_str = signer.unsign(request.POST.get("signed_app_data"), max_age=300)
    except:
         return JsonResponse({
            "ok": False,
            "error": "The signed data received was invalid. Please try the login process again. If this issue persists, please contact support."
        })
    
    try:
        data = json.loads(raw_data_str)
    except:
        return JsonResponse({
            "ok": False,
            "error": "The JSON data was not in the expected format. Please contact support."
        })

    user = User.objects.get(employee_id=data["user_upi"])
    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    