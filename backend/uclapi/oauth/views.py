from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core import signing
from django.core.signing import TimestampSigner
from django.utils.http import quote
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, \
    csrf_protect
import requests
import redis

import os
import json
import hmac
import hashlib
import base64

from dashboard.models import App, User
from .app_helpers import generate_random_verification_code
from .models import OAuthScope, OAuthToken
from uclapi.settings import REDIS_UCLAPI_HOST
from .decorators import oauth_token_check


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
    data = app.client_id + state
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
            "error": ("No signed app data returned from Shibboleth."
                      " Please use the authorise endpoint.")
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

    client_id = appdata[:33]
    state = appdata[33:]

    app = App.objects.get(client_id=client_id)

    try:
        eppn = request.META['HTTP_EPPN']
        groups = request.META['HTTP_UCLINTRANETGROUPS']
        cn = request.META['HTTP_CN']
        department = request.META['HTTP_DEPARTMENT']
        given_name = request.META['HTTP_GIVENNAME']
        display_name = request.META['HTTP_DISPLAYNAME']
        employee_id = request.META['HTTP_EMPLOYEEID']
    except KeyError:
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
    return render(request, 'permissions.html', {
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
            "error": ("The signed data received was invalid."
                      " Please try the login process again. "
                      "If this issue persists, please contact support.")
        })

    try:
        data = json.loads(raw_data_str)
    except:
        return JsonResponse({
            "ok": False,
            "error": ("The JSON data was not in the expected format."
                      " Please contact support.")
        })

    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    redir = app.callback_url + "?result=denied?state=" + state

    return redirect(redir)


@csrf_protect
def userallow(request):
    signer = TimestampSigner()

    try:
        raw_data_str = signer.unsign(
            request.POST.get("signed_app_data"), max_age=300)
    except (signing.BadSignature, KeyError):
        return JsonResponse({
            "ok": False,
            "error": ("The signed data received was invalid."
                      " Please try the login process again."
                      " If this issue persists, please contact support.")
        })

    try:
        data = json.loads(raw_data_str)
    except ValueError:
        return JsonResponse({
            "ok": False,
            "error": ("The JSON data was not in the expected format."
                      " Please contact support.")
        })

    user = User.objects.get(employee_id=data["user_upi"])
    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    # Now we have the data we need to generate a random code and
    # store it in redis along with the request properties.
    # Once the client is redirected to they can make a request
    # with that code to obtain an OAuth token. This can then
    # be used to obtain User Data.

    code = generate_random_verification_code()

    r = redis.StrictRedis(host=REDIS_UCLAPI_HOST)

    verification_data = {
        "client_id": app.client_id,
        "state": state,
        "upi": data["user_upi"]
    }

    verification_data_str = json.dumps(
        verification_data, cls=DjangoJSONEncoder)

    # Store this verification data in redis so that it can be obtained later
    # when the client wants to swap the code for a token.
    # The code will only be valid for 90 seconds after which redis will just
    # drop it and the process will be invalidated.
    r.set(code, verification_data_str, ex=90)

    # Now redirect the user back to the app, at long last.
    # Just in case they've tried to be super clever and host multiple apps with
    # the same callback URL, we'll provide the client ID along with the state
    return redirect(
            app.callback_url + "?result=allowed&code=" + code + "&client_id=" +
            app.client_id + "&state=" + state
        )


def token(request):
    try:
        code = request.GET.get("code")
        client_id = request.GET.get("client_id")
        validation_hmac = request.GET.get("client_secret_proof")
    except KeyError:
        return JsonResponse({
            "ok": False,
            "error": ("The client did not provide"
                      " the requisite data to get a token.")
        })

    r = redis.StrictRedis(host=REDIS_UCLAPI_HOST)
    try:
        data_json = r.get(code).decode('ascii')
    except:
        return JsonResponse({
            "ok": False,
            "error": ("The code received was invalid, or has expired."
                      " Please try again.")
        })

    data = json.loads(data_json)

    client_id = data["client_id"]
    state = data["state"]
    upi = data["upi"]

    app = App.objects.get(client_id=client_id)
    try:
        hmac_digest = hmac.new(
            bytes(app.client_secret, 'ascii'),
            msg=code.encode('ascii'),
            digestmod=hashlib.sha256).digest()
        hmac_b64 = base64.b64encode(hmac_digest).decode()
    except:
        return JsonResponse({
            "ok": False,
            "error": "HMAC failed. Please contact support."
        })

    if hmac_b64 != validation_hmac:
        return JsonResponse({
            "ok": False,
            "error": ("The HMAC check returned a different hash to"
                      " the proof that was supplied. "
                      "Please ensure that the client secret is correct"
                      " and that the digest is base64 encoded.")
        })

    # Assume now that the digest was correct,
    # and therefore the client secret is correct.
    # Carry on and assign a token

    user = User.objects.get(employee_id=upi)

    # Since the data has passed verification at this point, and we have
    # checked the validity of the client secret, we can
    # now generate an OAuth access token for the user.
    # But first, we should check if a token has been generated already.
    # If a token does already exist then we should not add yet another one to
    # the database. We can just pass those keys to the app
    # again (in case it has lost them).

    try:
        token = OAuthToken.objects.get(app=app, user=user)

        # If the code gets here then the user has used this app before,
        # so let's check that the scope does
        # not need changing
        if not token.scope.scopeIsEqual(app.scope):
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
        # The user has never logged in before so let's clone the scope and
        # create a brand new OAuth token

        # Clone the scope defined in the app model
        app_scope = app.scope
        app_scope.id = None
        app_scope.save()

        # Now set up a new token with that scope
        token = OAuthToken(
            app=app,
            user=user,
            scope=app_scope
        )
        token.save()

    # Now that we have a token we can pass one back to the app
    # We sincerely hope they'll save this token!
    # The app can use the token to pull in any personal data (name, UPI, etc.)
    # later on, so we won't bother to give it to them just yet.

    oauth_data = {
        "ok": True,
        "state": state,
        "client_id": app.client_id,
        "token": token.token,
        "scope": json.dumps(token.scope.scopeDict())
    }

    return JsonResponse(oauth_data)


@oauth_token_check([])
def userdata(request):
    try:
        token_code = request.GET.get("token")
        token = OAuthToken.objects.get(token=token_code)
    except ObjectDoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "Invalid token given"
        })

    return JsonResponse({
        "ok": True,
        "full_name": token.user.full_name,
        "email": token.user.email,
        "given_name": token.user.given_name,
        "cn": token.user.cn,
        "department": token.user.department,
        "upi": token.user.employee_id
    })
