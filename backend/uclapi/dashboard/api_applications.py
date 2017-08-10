import json
import os
import tldextract
from django.http import HttpResponseBadRequest

from oauth.scoping import Scopes
from django.http import HttpResponseBadRequest

from dashboard.tasks import keen_add_event_task as keen_add_event

from roombookings.helpers import PrettyJsonResponse

from .models import App, User


def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    return user


def create_app(request):
    if request.method != "POST":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        name = request.POST["name"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have name or user."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    new_app = App(name=name, user=user)
    new_app.save()

    keen_add_event.delay("App created", {
        "appid": new_app.id,
        "name": new_app.name,
        "userid": user.id
    })

    s = Scopes()

    return PrettyJsonResponse({
        "success": True,
        "message": "App sucessfully created",
        "app": {
            "name": new_app.name,
            "id": new_app.id,
            "token": new_app.api_token,
            "created": new_app.created,
            "updated": new_app.last_updated,
            "oauth": {
                "client_id": new_app.client_id,
                "client_secret": new_app.client_secret,
                "callback_url": new_app.callback_url,
                "scopes": s.get_all_scopes()
            }
        }
    })


def rename_app(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "error": "Request is not of method POST"
        }))

    try:
        app_id = request.POST["app_id"]
        new_name = request.POST["new_name"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id/new_name"
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = PrettyJsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.name = new_name
        app.save()

        keen_add_event.delay("App renamed", {
            "appid": app.id,
            "new_name": app.name,
            "userid": user.id
        })

        return PrettyJsonResponse({
            "success": True,
            "message": "App sucessfully renamed.",
            "date": app.last_updated
        })


def regenerate_app_token(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "error": "Request is not of method POST"
        }))

    try:
        app_id = request.POST["app_id"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = PrettyJsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.regenerate_token()
        new_api_token = app.api_token

        keen_add_event.delay("App token regenerated", {
            "appid": app.id,
            "userid": user.id
        })

        return PrettyJsonResponse({
            "success": True,
            "message": "App token sucessfully regenerated.",
            "app": {
                "id": app.id,
                "token": new_api_token,
                "date": app.last_updated
            }
        })


def delete_app(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "error": "Request is not of method POST"
        }))

    try:
        app_id = request.POST["app_id"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = PrettyJsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.delete()

        keen_add_event.delay("App deleted", {
            "appid": app_id,
            "userid": user.id
        })

        return PrettyJsonResponse({
            "success": True,
            "message": "App sucessfully deleted.",
        })


def set_callback_url(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "error": "Request is not of method POST"
        }))
    try:
        app_id = request.POST["app_id"]
        new_callback_url = request.POST["callback_url"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    # Check if the new callback URL uses an acceptable protocol
    # (e.g. HTTP or HTTPS)
    # The list comprehension will explode the
    # UCLAPI_OAUTH_CALLBACK_ALLOWED_PROTOCOLS environment
    # variable, split by semicolons, append each one with :// then
    # check if the URL starts with it.
    # If none of them work then bail out.
    if not any([new_callback_url.startswith(p + "://") for p in os.environ.get(
            "UCLAPI_OAUTH_CALLBACK_ALLOWED_PROTOCOLS").split(';')]):
        response = PrettyJsonResponse({
            "success": False,
            "message": ("The requested callback URL"
                        " does not use an acceptable protocol.")
        })
        response.status_code = 400
        return response

    url_data = tldextract.extract(new_callback_url)

    if any(
        [p == (url_data.domain + "." + url_data.suffix)
            for p in os.environ.get(
            "UCLAPI_OAUTH_CALLBACK_DENIED_URLS").split(';')]):
        response = PrettyJsonResponse({
            "success": False,
            "message": ("The requested callback URL"
                        " is hosted on a banned domain.")
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = PrettyJsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response

    app = apps[0]
    app.callback_url = new_callback_url
    app.save()

    keen_add_event.delay("App callback URL changed", {
        "appid": app_id,
        "userid": user.id,
        "newcallbackurl": new_callback_url
    })

    return PrettyJsonResponse({
        "success": True,
        "message": "Callback URL successfully changed.",
    })


def update_scopes(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "error": "Request is not of method POST"
        }))

    try:
        app_id = request.POST["app_id"]
        scopes_json = request.POST["scopes"]
        user_id = request.session["user_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    try:
        scopes = json.loads(scopes_json)
    except:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Invalid scope data that could not be parsed."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = PrettyJsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        current = app.scope.scope_number
        s = Scopes()
        try:
            for scope in scopes:
                if "checked" in scope and scope["checked"]:
                    current = s.add_scope(current, scope["name"])
                else:
                    current = s.remove_scope(current, scope["name"])

            app.scope.scope_number = current
            app.scope.save()
            app.save()
        except:
            response = PrettyJsonResponse({
                "success": False,
                "message": "Invalid scope data that could not be iterated."
            })
            response.status_code = 400
            return response

        keen_add_event.delay("App scopes changed", {
            "appid": app_id,
            "userid": user.id,
            "scopes": scopes
        })

        return PrettyJsonResponse({
            "success": True,
            "message": "Scope successfully changed",
        })
