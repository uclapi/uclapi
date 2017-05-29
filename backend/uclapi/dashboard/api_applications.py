from django.http import HttpResponseBadRequest, JsonResponse
from .models import App, User
import keen


def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    return user


def create_app(request):
    if request.method != "POST":
        response = JsonResponse({
            "success": False,
            "message": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        name = request.POST["name"]
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": "Request does not have name or user."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    new_app = App(name=name, user=user)
    new_app.save()

    keen.add_event("App created", {
        "appid": new_app.id,
        "name": new_app.name,
        "userid": user.id
    })

    return JsonResponse({
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
                "scope": {
                    "private_roombookings": new_app.scope.private_roombookings,
                    "private_timetable": new_app.scope.private_timetable,
                    "private_uclu": new_app.scope.private_uclu
                }
            }
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
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id/new_name"
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.name = new_name
        app.save()

        keen.add_event("App renamed", {
            "appid": app.id,
            "new_name": app.name,
            "userid": user.id
        })

        return JsonResponse({
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
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.regenerate_token()
        new_api_token = app.api_token

        keen.add_event("App token regenerated", {
            "appid": app.id,
            "userid": user.id
        })

        return JsonResponse({
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
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response

    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.delete()

        keen.add_event("App deleted", {
            "appid": app_id,
            "userid": user.id
        })

        return JsonResponse({
            "success": True,
            "message": "App sucessfully deleted.",
        })

def set_callback_url(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")
    
    try:
        app_id = request.POST["app_id"]
        new_callback_url = request.POST["callback_url"]
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response
    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.callback_url = new_callback_url
        app.save()

        keen.add_event("App callback URL changed", {
            "appid": app_id,
            "userid": user.id,
            "newcallbackurl": new_callback_url
        })

        return JsonResponse({
            "success": True,
            "message": "Callback URL successfully changed.",
        })

def set_rb_scope(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")
    
    try:
        app_id = request.POST["app_id"]
        scope_status = request.POST["scope_status"] == "true"
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response
    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.scope.private_roombookings = scope_status
        app.scope.save()

        keen.add_event("App room bookings scope changed", {
            "appid": app_id,
            "userid": user.id,
            "rbscope": scope_status
        })

        return JsonResponse({
            "success": True,
            "message": "Scope successfully changed",
        })

def set_timetable_scope(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")
    
    try:
        app_id = request.POST["app_id"]
        scope_status = request.POST["scope_status"] == "true"
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response
    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.scope.private_timetable = scope_status
        app.scope.save()

        keen.add_event("App timetable scope changed", {
            "appid": app_id,
            "userid": user.id,
            "timetablescope": scope_status
        })

        return JsonResponse({
            "success": True,
            "message": "Scope successfully changed",
        })

def set_uclu_scope(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")
    
    try:
        app_id = request.POST["app_id"]
        scope_status = request.POST["scope_status"] == "true"
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": "Request does not have app_id."
        })
        response.status_code = 400
        return response
    user = get_user_by_id(user_id)

    apps = App.objects.filter(id=app_id, user=user)
    if len(apps) == 0:
        response = JsonResponse({
            "success": False,
            "message": "App does not exist."
        })
        response.status_code = 400
        return response
    else:
        app = apps[0]
        app.scope.private_uclu = scope_status
        app.scope.save()

        keen.add_event("App UCLU scope changed", {
            "appid": app_id,
            "userid": user.id,
            "ucluscope": scope_status
        })

        return JsonResponse({
            "success": True,
            "message": "Scope successfully changed",
        })