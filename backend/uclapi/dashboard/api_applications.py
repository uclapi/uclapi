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
            "message": "Request is not of method POST"
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

    return PrettyJsonResponse({
        "success": True,
        "message": "App sucessfully created",
        "app": {
            "id": new_app.id,
            "token": new_app.api_token,
            "created": new_app.created,
            "updated": new_app.last_updated
        }
    })


def rename_app(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")

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
        return HttpResponseBadRequest("Error: Request is not of method POST")

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
        return HttpResponseBadRequest("Error: Request is not of method POST")

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
