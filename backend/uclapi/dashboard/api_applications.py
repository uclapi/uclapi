import json

from dashboard.tasks import keen_add_event_task as keen_add_event
from oauth.scoping import Scopes
from roombookings.helpers import PrettyJsonResponse

from .app_helpers import is_url_safe
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
    except KeyError:
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
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

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
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method POST"
        })
        response.status_code = 400
        return response

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
        app.deleted = True
        app.save()

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
    except KeyError:
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

    if not is_url_safe(new_callback_url):
        response = PrettyJsonResponse({
            "success": False,
            "message": ("The requested callback URL"
                        " is not valid.")
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
    except KeyError:
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
        except (KeyError, ValueError):
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
