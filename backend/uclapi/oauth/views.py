from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core import signing
from django.core.signing import TimestampSigner
from django.utils.http import quote
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

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
            "full_name": given_name,
            "eppn": eppn
        }
    }

    initial_data = json.dumps(page_data, cls=DjangoJSONEncoder)
    return render(request, 'permissions.html',
    {
        'initial_data': initial_data
    })
    # return JsonResponse(page_data)