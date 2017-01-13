from django.http import HttpResponseBadRequest, JsonResponse
from .models import App, User


def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    return user


def create_app(request):
    if request.type != "POST":
        response = JsonResponse({
            "success": False,
            "message": "Request is not of type POST"
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

    return JsonResponse({
        "success": True,
        "message": "App sucessfully created",
        "app": {
            "id": new_app.id,
            "token": new_app.api_token
        }
    })


def rename_app(request):
    if request.type != "POST":
        return HttpResponseBadRequest("Error: Request is not of type POST")

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

        return JsonResponse({
            "success": True,
            "message": "App sucessfully renamed.",
        })


def regenerate_app_token(request):
    if request.type != "POST":
        return HttpResponseBadRequest("Error: Request is not of type POST")

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

        return JsonResponse({
            "success": True,
            "message": "App sucessfully renamed.",
            "app": {
                "id": app.id,
                "token": new_api_token
            }
        })


def delete_app(request):
    if request.type != "POST":
        return HttpResponseBadRequest("Error: Request is not of type POST")

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

        return JsonResponse({
            "success": True,
            "message": "App sucessfully deleted.",
        })
