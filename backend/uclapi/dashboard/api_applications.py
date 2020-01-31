import json

from oauth.scoping import Scopes
from common.helpers import PrettyJsonResponse

from .app_helpers import (is_url_unsafe, NOT_HTTPS,
                          NOT_VALID, URL_BLACKLISTED, NOT_PUBLIC)
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
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have name or user."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    new_app = App(name=name, user=user)
    new_app.save()

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
            },
            "webhook": {
                "verification_secret": new_app.webhook.verification_secret,
            }
        }
    })


def rename_app(request):
    if request.method != "POST":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        app_id = request.POST["app_id"]
        new_name = request.POST["new_name"]
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have app_id/new_name"
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user, deleted=False)
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

        return PrettyJsonResponse({
            "success": True,
            "message": "App sucessfully renamed.",
            "date": app.last_updated
        })


def regenerate_app_token(request):
    if request.method != "POST":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        app_id = request.POST["app_id"]
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have an app_id."
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
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        app_id = request.POST["app_id"]
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have an app_id."
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
        app.deleted = True
        webhook = app.webhook
        webhook.url = ""
        webhook.siteid = ""
        webhook.roomid = ""
        webhook.contact = ""
        webhook.enabled = False
        webhook.save()
        app.save()

        return PrettyJsonResponse({
            "success": True,
            "message": "App sucessfully deleted.",
        })


def set_callback_url(request):
    if request.method != "POST":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response
    try:
        app_id = request.POST["app_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have an app_id."
        })
        response.status_code = 400
        return response

    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "User ID not set in session. Please log in again."
        })
        response.status_code = 400
        return response

    try:
        new_callback_url = request.POST["callback_url"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have a Callback URL."
        })
        response.status_code = 400
        return response
    url_not_safe_saved = is_url_unsafe(new_callback_url)
    if url_not_safe_saved:
        if url_not_safe_saved == NOT_HTTPS:
            message = "The requested callback URL does not "\
                      "start with 'https://'."
        elif url_not_safe_saved == NOT_VALID:
            message = "The requested callback URL is not valid."
        elif url_not_safe_saved == URL_BLACKLISTED:
            message = "The requested callback URL is forbidden."
        elif url_not_safe_saved == NOT_PUBLIC:
            message = "The requested callback URL is not publicly available."
        response = PrettyJsonResponse({
            "success": False,
            "message": message
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

    return PrettyJsonResponse({
        "success": True,
        "message": "Callback URL successfully changed.",
    })


def update_scopes(request):
    if request.method != "POST":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        app_id = request.POST["app_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "Request does not have an app_id."
        })
        response.status_code = 400
        return response

    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        response = PrettyJsonResponse({
            "success": False,
            "message": "User ID not set in session. Please log in again."
        })
        response.status_code = 400
        return response

    try:
        scopes_json = request.POST["scopes"]
    except KeyError:
        response = PrettyJsonResponse({
            "success": False,
            "message": "No scopes data attached."
        })
        response.status_code = 400
        return response

    try:
        scopes = json.loads(scopes_json)
    except ValueError:
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
        except (KeyError, ValueError, TypeError):
            response = PrettyJsonResponse({
                "success": False,
                "message": "Invalid scope data that could not be iterated."
            })
            response.status_code = 400
            return response

        return PrettyJsonResponse({
            "success": True,
            "message": "Scope successfully changed.",
        })
