import json
import os
import requests

import redis
from django.core import signing
from django.core.serializers.json import DjangoJSONEncoder
from django.core.signing import TimestampSigner
from django.shortcuts import redirect, render
from django.utils.http import quote
from django.views.decorators.csrf import (
    csrf_exempt,
    csrf_protect,
    ensure_csrf_cookie
)

from dashboard.models import App, User

from .app_helpers import (
    generate_random_verification_code,
    get_student_by_upi,
    validate_azure_ad_callback
)
from .models import OAuthToken
from .scoping import Scopes

from uclapi.settings import REDIS_UCLAPI_HOST
from common.decorators import uclapi_protected_endpoint, get_var
from common.helpers import PrettyJsonResponse


# The endpoint that creates an Azure AD login and redirects the user to it
def authorise(request):
    client_id = request.GET.get("client_id", None)
    state = request.GET.get("state", None)
    if not (client_id and state):
        response = PrettyJsonResponse({
            "ok": False,
            "error": "incorrect parameters supplied"
        })
        response.status_code = 400
        return response

    try:
        # We only allow the process to happen if the app exists and has not
        # been flagged as deleted
        app = App.objects.filter(client_id=client_id, deleted=False)[0]
    except IndexError:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "App does not exist for client id"
        })
        response.status_code = 400
        return response

    if app.callback_url is None or app.callback_url.strip() == "":
        response = PrettyJsonResponse({
            "ok": False,
            "error": (
                "This app does not have a callback URL set. "
                "If you are the developer of this app, "
                "please ensure you have set a valid callback "
                "URL for your application in the Dashboard. "
                "If you are a user, please contact the app's "
                "developer to rectify this."
            )
        })
        response.status_code = 400
        return response

    # Sign the app and state pair before heading to AD to help protect
    # against CSRF and XSS attacks
    signer = TimestampSigner()
    data = app.client_id + state
    signed_data = signer.sign(data)

    # Build Azure AD callback URL
    query = {
        'client_id': os.environ.get("AZURE_AD_CLIENT_ID"),
        'response_type': 'code',
        'redirect_uri': 'https://uclapi.com/oauth/adcallback',
        'scope': 'openid email profile',
        'response_mode': 'query',
        'state': signed_data,
    }

    url = os.environ.get("AZURE_AD_ROOT") + \
        "/oauth2/v2.0/authorize?" + urlencode(query)

    # Send the user to AD to log in
    return redirect(url)


def exchange_azure_ad_auth_code(code):
    url = os.environ.get("AZURE_AD_ROOT") + "/oauth2/v2.0/token"
    body = {
        'client_id': os.environ.get("AZURE_AD_CLIENT_ID"),
        'code': code,
        'redirect_uri': 'https://uclapi.com/oauth/adcallback',
        'grant_type': 'authorization_code',
        'client_secret': os.environ.get("AZURE_AD_CLIENT_SECRET"),
    }
    response = requests.post(url, data=body)
    if response.status_code != 200:
        return None

    return response.json()


@csrf_exempt
@ensure_csrf_cookie
def adcallback(request):
    # Callback from AD login

    appdata_signed = request.GET.get("state", None)
    if not appdata_signed:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("No signed app data returned from Azure AD."
                      " Please use the authorise endpoint.")
        })
        response.status_code = 400
        return response

    signer = TimestampSigner()
    try:
        # Expire our signed tokens after five minutes for added security
        appdata = signer.unsign(appdata_signed, max_age=300)
    except signing.SignatureExpired:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("Login data has expired. Please attempt to log in "
                      "again. If the issues persist please contact the "
                      "UCL API Team to rectify this.")
        })
        response.status_code = 400
        return response
    except signing.BadSignature:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("Bad signature. Please attempt to log in again. "
                      "If the issues persist please contact the UCL API "
                      "Team to rectify this.")
        })
        response.status_code = 400
        return response

    azure_token_data = exchange_azure_ad_auth_code(
        request.GET.get("code"))

    if not azure_token_data:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("Failed to authenticate with Azure AD. Please attempt to log in again. "
                      "If the issues persist please contact the UCL API "
                      "Team to rectify this.")
        })
        response.status_code = 400
        return response

    client_id = appdata[:33]
    state = appdata[33:]

    # We can trust this value because it was extracted from the signed data
    # string sent via Azure AD
    app = App.objects.get(client_id=client_id)

    validation_result = validate_azure_ad_callback(request)
    if isinstance(validation_result, str):
        response = PrettyJsonResponse({
            "ok": False,
            "error": validation_result
        })
        response.status_code = 400
        return response
    else:
        user = validation_result

    # Log the user into the system using their User ID
    request.session["user_id"] = user.id

    signer = TimestampSigner()
    response_data = {
        "client_id": app.client_id,
        "state": state,
        "user_upi": user.employee_id
    }

    response_data_str = json.dumps(response_data, cls=DjangoJSONEncoder)
    response_data_signed = signer.sign(response_data_str)

    s = Scopes()

    page_data = {
        "app_name": app.name,
        "creator": app.user.full_name,
        "client_id": app.client_id,
        "state": state,
        "scopes": s.scope_dict(app.scope.scope_number),
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

    try:
        token = OAuthToken.objects.get(app=app, user=user)
    except OAuthToken.DoesNotExist:
        return render(request, 'permissions.html', {
            'initial_data': initial_data
        })

    if token.scope.scopeIsEqual(app.scope) and token.active:
        code = generate_random_verification_code()

        r = redis.Redis(host=REDIS_UCLAPI_HOST)

        verification_data = {
            "client_id": app.client_id,
            "state": state,
            "upi": user.employee_id
        }

        verification_data_str = json.dumps(
            verification_data, cls=DjangoJSONEncoder)

        # Store this verification data in redis so that it can be obtained
        # later when the client wants to swap the code for a token.
        # The code will only be valid for 90 seconds after which redis will
        # just drop it and the process will be invalidated.
        r.set(code, verification_data_str, ex=90)

        # Now redirect the user back to the app, at long last.
        # Just in case they've tried to be super clever and host multiple
        # apps with the same callback URL, we'll provide the client ID
        # along with the state
        return redirect(
            app.callback_url + "?result=allowed&code=" + code
            + "&client_id=" + app.client_id + "&state=" + state
        )
    else:
        return render(request, 'permissions.html', {
            'initial_data': initial_data
        })


@csrf_protect
def userdeny(request):
    signer = TimestampSigner()

    try:
        signed_data = request.POST.get("signed_app_data")
        raw_data_str = signer.unsign(signed_data, max_age=300)
    except (signing.BadSignature, KeyError, TypeError):
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The signed data received was invalid."
                      " Please try the login process again. "
                      "If this issue persists, please contact us at "
                      "isd.apiteam@ucl.ac.uk or on github.")
        })
        response.status_code = 400
        return response

    try:
        data = json.loads(raw_data_str)
    except Exception:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The JSON data was not in the expected format."
                      " Please contact us at "
                      "isd.apiteam@ucl.ac.uk or on github.")
        })
        response.status_code = 400
        return response

    # We can trust this value because it came from a signed dictionary
    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    redir = "{}?result=denied&state={}".format(app.callback_url, state)

    # Now check if a token has been granted in the past. If so, invalidate it.
    # There shouldn't be a situation where more than one user/app token pair
    # exists but, just in case, let's invalidate them all.
    try:
        users = User.objects.filter(employee_id=data["user_upi"])
        user = users[0]
    except (User.DoesNotExist, KeyError, IndexError):
        response = PrettyJsonResponse({
            "ok": False,
            "error":
                "User does not exist. This should never occur. "
                "Please contact us at "
                "isd.apiteam@ucl.ac.uk or on github."
        })
        response.status_code = 400
        return response

    tokens = OAuthToken.objects.filter(app=app, user=user)
    for token in tokens:
        token.active = False
        token.save()

    # Send the user to the app's denied permission page
    return redirect(redir)


@csrf_protect
def userallow(request):
    signer = TimestampSigner()

    try:
        raw_data_str = signer.unsign(
            request.POST.get("signed_app_data"), max_age=300)
    except (signing.BadSignature, KeyError, TypeError):
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The signed data received was invalid."
                      " Please try the login process again."
                      " If this issue persists, please contact us at"
                      " isd.apiteam@ucl.ac.uk or on github.")
        })
        response.status_code = 400
        return response

    try:
        data = json.loads(raw_data_str)
    except ValueError:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The JSON data was not in the expected format."
                      " Please contact us at"
                      " isd.apiteam@ucl.ac.uk or on github.")
        })
        response.status_code = 400
        return response

    # We can trust this app value because it was sent from a signed
    # data dictionary
    app = App.objects.get(client_id=data["client_id"])
    state = data["state"]

    # Now we have the data we need to generate a random code and
    # store it in redis along with the request properties.
    # Once the client is redirected to they can make a request
    # with that code to obtain an OAuth token. This can then
    # be used to obtain User Data.

    code = generate_random_verification_code()

    r = redis.Redis(host=REDIS_UCLAPI_HOST)

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
        app.callback_url + "?result=allowed&code=" + code + "&client_id="
        + app.client_id + "&state=" + state
    )


@csrf_exempt
def token(request):
    code = get_var(request, "code")
    client_id = get_var(request, "client_id")
    client_secret = get_var(request, "client_secret")

    if not code or not client_id or not client_secret:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The client did not provide"
                      " the requisite data to get a token.")
        })
        response.status_code = 400
        return response

    r = redis.Redis(host=REDIS_UCLAPI_HOST)
    try:
        data_json = r.get(code).decode('ascii')

    except Exception:
        response = PrettyJsonResponse({
            "ok": False,
            "error": ("The code received was invalid, or has expired."
                      " Please try again.")
        })
        response.status_code = 400
        return response

    # Remove code from Redis once used to protect against replay attacks.
    # This is in a try...except to prevent against the edge case when the
    # code has expired between getting and deleting.
    try:
        r.delete(code)
    except Exception:
        pass

    data = json.loads(data_json)

    client_id = data["client_id"]
    state = data["state"]
    upi = data["upi"]

    try:
        app = App.objects.filter(client_id=client_id, deleted=False)[0]
    except IndexError:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "App has been deleted or the Client ID is invalid."
        })
        response.status_code = 400
        return response

    if app.client_secret != client_secret:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "Client secret incorrect"
        })
        response.status_code = 400
        return response

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

        # If the user has denied this app access before and invalidated a token
        # then let's re-enabled that token because access is permitted again.
        if token.active is False:
            token.active = True
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

    s = Scopes()

    oauth_data = {
        "ok": True,
        "state": state,
        "client_id": app.client_id,
        "token": token.token,
        "access_token": token.token,
        "scope": json.dumps(s.scope_dict(token.scope.scope_number))
    }

    return PrettyJsonResponse(oauth_data)


@uclapi_protected_endpoint(
    personal_data=True,
    last_modified_redis_key="timetable_gencache"
)
def userdata(request, *args, **kwargs):
    token = kwargs['token']
    try:
        get_student_by_upi(
            token.user.employee_id
        )
        is_student = True
    except IndexError:
        is_student = False

    user_data = {
        "ok": True,
        "cn": token.user.cn,
        "department": token.user.department,
        "email": token.user.email,
        "full_name": token.user.full_name,
        "given_name": token.user.given_name,
        "upi": token.user.employee_id,
        "scope_number": token.scope.scope_number,
        "is_student": is_student,
        "ucl_groups": token.user.raw_intranet_groups.split(';'),
        "sn": token.user.sn,
        "mail": token.user.mail
    }

    return PrettyJsonResponse(
        user_data,
        custom_header_data=kwargs
    )


def scope_map(request):
    s = Scopes()
    scope_map = {
        "scope_map": s.get_scope_map()
    }
    return PrettyJsonResponse(scope_map)


@uclapi_protected_endpoint(
    personal_data=True,
    last_modified_redis_key=None
)
def token_test(request, *args, **kwargs):
    s = Scopes()

    token = kwargs['token']

    return PrettyJsonResponse({
        "ok": True,
        "active": token.active,
        "user_upi": token.user.employee_id,
        "scopes": s.scope_dict_all(
            current=token.scope.scope_number,
            pretty_print=False
        ),
        "scope_number": token.scope.scope_number
    }, custom_header_data=kwargs)


@uclapi_protected_endpoint(
    personal_data=True,
    required_scopes=['student_number'],
    last_modified_redis_key="timetable_gencache"
)
def get_student_number(request, *args, **kwargs):
    token = kwargs['token']

    try:
        student_data = get_student_by_upi(
            token.user.employee_id
        )
    except IndexError:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "User is not a student."
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    data = {
        "ok": True,
        "student_number": student_data.studentid
    }
    return PrettyJsonResponse(
        data,
        custom_header_data=kwargs
    )


@csrf_exempt
def settings_shibboleth_callback(request):
    # should auth user login or signup
    # then redirect to my apps homepage

    validation_result = validate_shibboleth_callback(request)
    if isinstance(validation_result, str):
        response = PrettyJsonResponse({
            "ok": False,
            "error": validation_result
        })
        response.status_code = 400
        return response
    else:
        request.session["user_id"] = validation_result.id
        return redirect(settings)


@ensure_csrf_cookie
def settings(request):
    # Check whether the user is logged in
    try:
        request.session["user_id"]
    except KeyError:
        # Build Shibboleth callback URL
        url = os.environ["SHIBBOLETH_ROOT"] + "/Login?target="
        param = (request.build_absolute_uri(request.path)
                 + "user/login.callback")
        param = quote(param)
        url = url + param

        return redirect(url)

    return render(request, 'settings.html')


@ensure_csrf_cookie
def get_settings(request):
    if request.method != "GET":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Must be a GET request"
        })
        response.status_code = 400
        return response

    # Check whether the user is logged in
    try:
        user_id = request.session["user_id"]
    except KeyError:
        # Build Shibboleth callback URL
        url = os.environ["SHIBBOLETH_ROOT"] + "/Login?target="
        param = (request.build_absolute_uri(request.path)
                 + "user/login.callback")
        param = quote(param)
        url = url + param

        return redirect(url)

    user = User.objects.get(id=user_id)

    tokens = OAuthToken.objects.filter(user=user)

    authorised_apps = []
    scopes = Scopes()

    for token in tokens:
        authorised_apps.append({
            "id": token.id,
            "active": token.active,
            "app": {
                "id": token.app.id,
                "creator": {
                    "name": token.app.user.full_name,
                    "email": token.app.user.email
                },
                "client_id": token.app.client_id,
                "name": token.app.name,
                "scopes": scopes.scope_dict_all(token.scope.scope_number)
            }
        })

    initial_data_dict = {
        "status": "ONLINE",
        "fullname": user.full_name,
        "user_id": user.id,
        "department": user.department,
        "scopes": scopes.get_scope_map(),
        "apps": authorised_apps
    }

    return PrettyJsonResponse(initial_data_dict)


@ensure_csrf_cookie
def deauthorise_app(request):
    # Find which user is requesting to deauthorise an app
    user = User.objects.get(id=request.session["user_id"])

    # Find the app that the user wants to deauthorise
    client_id = request.GET.get("client_id", None)

    if client_id is None:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "A Client ID must be provided to deauthorise an app."
        })
        response.status_code = 400
        return response

    try:
        # We only allow the process to happen if the app exists and has not
        # been flagged as deleted
        app = App.objects.filter(client_id=client_id, deleted=False)[0]
    except IndexError:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "App does not exist with the Client ID provided."
        })
        response.status_code = 400
        return response

    try:
        token = OAuthToken.objects.get(app=app, user=user)
    except OAuthToken.DoesNotExist:
        response = PrettyJsonResponse({
            "ok": False,
            "error": (
                "The app with the Client ID provided does not have a "
                "token for this user, so no action was taken."
            )
        })
        response.status_code = 400
        return response

    token.delete()

    response = PrettyJsonResponse({
        "ok": True,
        "message": "App successfully deauthorised."
    })
    response.status_code = 200
    return response


@ensure_csrf_cookie
def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass

    response = redirect('/warning', )
    return response
