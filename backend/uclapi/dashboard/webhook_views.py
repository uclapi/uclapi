import os
import textwrap
from binascii import hexlify

import keen
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse

from .models import App, User, Webhook


def user_owns_app(user_id, app_id):
    user = User.objects.get(id=user_id)
    try:
        app = App.objects.get(id=app_id)
    except ObjectDoesNotExist:
        return False
    return app.user == user


def generate_ownership_verification_secret():
    key = hexlify(os.urandom(30)).decode()
    dashes_key = '-'.join(textwrap.wrap(key, 15))

    return dashes_key


def verify_ownership(webhook_url, ownership_verification_secret):
    payload = {
        "event": "webhook_verification"
    }
    req = requests.post(webhook_url, json=payload)
    try:
        resp = req.json()
    #TODO: check whether this is the right error to except
    except ValueError:
        return False
    else:
        return (
            resp["ownership_verification_secret"] ==
            ownership_verification_secret
        )


def create_webhook(request):
    if request.method != "POST":
        response = JsonResponse({
            "success": False,
            "message": "Request is not of method POST"
        })
        response.status_code = 400
        return response

    try:
        app_id = request.POST["app_id"]
        url = request.POST["url"]
        siteid = request.POST["siteid"]
        roomid = request.POST["roomid"]
        contact = request.POST["contact"]
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": (
                "Request is missing parameters. Should have app_id"
                ", url, siteid, roomid, contact as well as a sessionid cookie"
            )
        })
        response.status_code = 400
        return response

    if not user_owns_app(user_id, app_id):
        response = JsonResponse({
            "success": False,
            "message": (
                "App does not exist or user is lacking permission."
            )
        })
        response.status_code = 400
        return response

    # make sure this is a good URL
    if not verify_ownership(url, generate_ownership_verification_secret()):
        response = JsonResponse({
            "success": False,
            "message": (
                "Ownership of webhook can't be verified."
                # TODO: change this
                "[Link to relevant docs here]"
            )
        })
        response.status_code = 400
        return response

    app = App.objects.get(id=app_id)

    new_webhook = Webhook(
        app=app,
        url=url,
        siteid=siteid,
        roomid=roomid,
        contact=contact
    )
    new_webhook.save()

    keen.add_event("Webhook created", {
        "webhookid": new_webhook.id,
        "url": new_webhook.url,
        "appid": app_id
    })

    return JsonResponse({
        "success": True,
        "message": "Webhook sucessfully created",
        "webhook": {
            "id": new_webhook.id,
            "created": new_webhook.created,
            "updated": new_webhook.last_updated
        }
    })


def edit_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Error: Request is not of method POST")

    try:
        app_id = request.POST["app_id"]
        new_webhook_url = request.POST["new_webhook_url"]
        new_siteid = request.POST["new_siteid"]
        new_roomid = request.POST["new_roomid"]
        new_contact = request.POST["new_contact"]
        user_id = request.session["user_id"]
    except KeyError:
        response = JsonResponse({
            "success": False,
            "message": (
                "Request is missing parameters. Should have app_id"
                ", new_webhook_url, new_siteid, new_roomid, new_contact"
                " as well as a sessionid cookie"
            )
        })
        response.status_code = 400
        return response

    if not user_owns_app(user_id, app_id):
        response = JsonResponse({
            "success": False,
            "message": (
                "App does not exist or user is lacking permission."
            )
        })
        response.status_code = 400
        return response

    app = App.objects.get(id=app_id)
    webhook = app.webhook

    if new_webhook_url != webhook.url:
        # make sure this is a good URL
        if not verify_ownership(
            new_webhook_url, generate_ownership_verification_secret()
        ):
            response = JsonResponse({
                "success": False,
                "message": (
                    "Ownweship of webhook can't be verified."
                    "[Link to relevant docs here]"
                )
            })
            response.status_code = 400
            return response

    webhook.siteid = new_siteid
    webhook.roomid = new_roomid
    webhook.contact = new_contact

    keen.add_event("Webhook edited", {
        "appid": app.id,
        "userid": user_id,
        "new_webhook_url": new_webhook_url,
        "new_siteid": new_siteid,
        "new_roomid": new_roomid,
        "new_contact": new_contact,
    })

    return JsonResponse({
        "success": True,
        "message": "Webhook sucessfully changed.",
    })


def delete_webhook(request):
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

    if not user_owns_app(user_id, app_id):
        response = JsonResponse({
            "success": False,
            "message": (
                "App does not exist or user is lacking permission."
            )
        })
        response.status_code = 400
        return response

    app = App.objects.get(id=app_id)
    webhook = app.webhook
    webhook.delete()

    keen.add_event("Webhook deleted", {
        "appid": app_id,
        "userid": user_id,
        "webhook_url": webhook.url
    })

    return JsonResponse({
        "success": True,
        "message": "Webhook sucessfully deleted.",
    })
