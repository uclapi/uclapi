from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core import signing
from django.core.signing import TimestampSigner
from django.utils.http import quote
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
import requests

import os
import json

from dashboard.models import App, User
from .app_helpers import generate_random_verification_code
from .models import OAuthScope, OAuthToken

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

    redir = app.callback_url + "/denied?state=" + state
    
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

    # Now we have the data we need to generate a random code and send this to the backend along
    # with the state and request the app's client secret. If this matches we can generate OAuth
    # keys and pass them to the backend

    code = generate_random_verification_code()
    verification_data = {
        "verification_code": code,
        "client_id": app.client_id,
        "state": state
    }

    verification_data_str = json.dumps(verification_data, cls=DjangoJSONEncoder)
    verification_data_str_enc = signer.sign(verification_data_str)

    full_verification_data = {
        "data": verification_data_str,
        "client_id": app.client_id,
        "state": state,
        "verification_data": verification_data_str_enc
    }

    try:
        vr = requests.post(app.callback_url + "/verify", data=full_verification_data)
        verification_response = vr.json()

    except:
        return JsonResponse({
            "ok": False,
            "error": "The client did not respond with valid JSON. Please contact the application vendor."
        })

    try:
        if not verification_response["client_secret"] == app.client_secret:
            return JsonResponse({
                "ok": False,
                "error": "The secret the client returned was invalid. Please contact the application vendor."
            })
    except:
        return JsonResponse({
            "ok": False,
            "error": "The data the client returned was invalid. Please contact the application vendor."
        })

    # Only trust that the data was properly returned if the signature was 60 seconds ago
    try:
        data_check = signer.unsign(verification_response["verification_data"], 60)
    except:
        return JsonResponse({
            "ok": False,
            "error": "The signed data received failed the signature check. Either the server did not respond in a timely manner, or the data was tampered with."
        })

    # Since the data has passed verification at this point, and we have checked the validity of the client secret, we can
    # now generate an OAuth access token for the user.
    # But first, we should check if a token has been generated already.
    # If a token does already exist then we should not add yet another one to the database. We can just pass those keys to the app
    # again (in case it has lost them).

    try:
        token = OAuthToken.objects.get(app=app, user=user)

        # If the code gets here then the user has used this app before, so let's check that the scope does
        # not need changing
        if not token.scopeIsEqual(app.scope):
            # Remove the current scope from the token
            token.scope.delete()

            # Clone the scope of the app
            app_scope = app.scope
            app_scope.id = None
            app_scope.save()

            # Assign the new scope to the token
            token.scope = app_scope

            # Save the token with the new scope
            token.save()

    except OAuthToken.DoesNotExist:
        # The user has never logged in before so let's clone the scope and create a brand new
        # OAuth token

        # Clone the scope defined in the app model
        app_scope = app.scope
        app_scope.id = None
        app_scope.save()

        # Now set up a new token with that scope
        token = Token(
            app=app,
            user=user,
            scope=app_scope
        )
        token.save()

    # Now that we have a token we can pass one back to the app
    # We'll make a final HTTP request to the app and provide the state and the OAuth token.
    # We sincerely hope they'll save this token!
    # The app can use the token to pull in any personal data (name, UPI, etc.) later on, so
    # we won't bother to give it to them just yet.

    oauth_data = {
        "state": state,
        "client_id": app.client_id,
        "token": token.token,
        "scope": token.scope.scopeDict()
    }

    # Now forward them the OAuth token for the user. If they're not happy with that then
    # that's their fault after the final redirect!
    oauth_req = requests.post(app.callback_url + "/token", data=oauth_data)

    # Now redirect the user back to the app, at long last.
    # Just in case they've tried to be super clever and host multiple apps with the same
    # callback URL, we'll provide the client ID along with the state
    return redirect(app.callback_url + "?client_id=" + app.client_id + "&state=" + state)