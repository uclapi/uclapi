from common.helpers import PrettyJsonResponse
from .models import App, User
import requests
from .app_helpers import NOT_HTTPS, NOT_VALID, URL_BLACKLISTED, generate_secret, is_url_unsafe, get_session_user_cn
from dashboard.api_applications import get_user_by_cn

from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

def user_owns_app(user_id, app_id):
    user = User.objects.get(id=user_id)
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        return False
    return app.user == user


def verify_ownership(webhook_url, ownership_challenge, verification_secret):
    payload = {
        "service": "webhook",
        "name": "challenge",
        "challenge": ownership_challenge,
        "verification_secret": verification_secret,
    }

    try:
        req = requests.post(webhook_url, json=payload, timeout=3)
        resp = req.json()
    except (ValueError, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return False
    else:
        if "challenge" not in resp.keys():
            return False
        return (resp["challenge"] == ownership_challenge)


@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def edit_webhook(request):
    if request.method != "POST" or request.headers['Content-Type'] != 'application/json':
        response = PrettyJsonResponse({"ok": False, "message": ("Request is not of method POST")})
        response.status_code = 400
        return response

    try:
        app_id = request.data["app_id"]
        url = request.data["url"]
        siteid = request.data["siteid"]
        roomid = request.data["roomid"]
        contact = request.data["contact"]
    except KeyError:
        response = PrettyJsonResponse({
            "ok":
            False,
            "message": ("Request is missing parameters. Should have app_id"
                        ", url, siteid, roomid, contact")
        })
        response.status_code = 400
        return response

    try:
        user_cn = get_session_user_cn(request)
        user = get_user_by_cn(user_cn)
    except (KeyError, User.DoesNotExist):
        response = PrettyJsonResponse({
            "ok": False,
            "message": "User ID not set in session. Please log in again."
        })
        response.status_code = 400
        return response

    if not user_owns_app(user.id, app_id):
        response = PrettyJsonResponse({"ok": False, "message": ("App does not exist or user is lacking permission.")})
        response.status_code = 400
        return response

    app = App.objects.get(id=app_id)
    webhook = app.webhook

    if url != webhook.url:
        if is_url_unsafe(url) in [NOT_HTTPS, NOT_VALID, URL_BLACKLISTED]:
            response = PrettyJsonResponse({"ok": False, "message": ("Invalid URL")})
            response.status_code = 400
            return response

        if not verify_ownership(url, generate_secret(), webhook.verification_secret):
            response = PrettyJsonResponse({
                "ok":
                False,
                "message": ("Ownership of webhook can't be verified."
                            "Make sure to follow the documentation: "
                            "https://uclapi.com/docs#webhook/challenge-event")
            })
            response.status_code = 400
            return response

        webhook.url = url
        webhook.save()

    webhook.siteid = siteid
    webhook.roomid = roomid
    webhook.contact = contact
    webhook.enabled = True
    webhook.save()

    return PrettyJsonResponse({
        "ok": True,
        "message": "Webhook sucessfully changed.",
        "url": webhook.url,
        "roomid": webhook.roomid,
        "siteid": webhook.siteid,
        "contact": webhook.contact
    })


@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def refresh_verification_secret(request):
    if request.method != "POST" or request.headers['Content-Type'] != 'application/json':
        response = PrettyJsonResponse({"ok": False, "message": ("Request is not of method POST")})
        response.status_code = 400
        return response

    try:
        app_id = request.data["app_id"]
    except KeyError:
        response = PrettyJsonResponse({
            "ok":
            False,
            "message": ("Request is missing parameters. Should have app_id")
        })
        response.status_code = 400
        return response

    try:
        user_cn = get_session_user_cn(request)
        user = get_user_by_cn(user_cn)
    except (KeyError, User.DoesNotExist):
        response = PrettyJsonResponse({
            "ok": False,
            "message": "User ID not set in session. Please log in again."
        })
        response.status_code = 400
        return response

    if not user_owns_app(user.id, app_id):
        response = PrettyJsonResponse({"ok": False, "message": ("App does not exist or user is lacking permission.")})
        response.status_code = 400
        return response

    app = App.objects.get(id=app_id)
    webhook = app.webhook

    new_secret = generate_secret()
    webhook.verification_secret = new_secret
    webhook.save()

    return PrettyJsonResponse({"ok": True, "new_secret": new_secret})
