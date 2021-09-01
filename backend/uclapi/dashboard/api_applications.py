import json
import redis
from django.db.models import Count

from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.datetime_safe import datetime

from oauth.models import OAuthToken
from oauth.scoping import Scopes
from common.helpers import PrettyJsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST

from .app_helpers import (is_url_unsafe, NOT_HTTPS,
                          NOT_VALID, URL_BLACKLISTED, NOT_PUBLIC)
from .models import App, User, APICall


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
            },
            "analytics": {
                "requests": 0,
                "remaining_quota": User._meta.get_field('oauth_quota').get_default(),
                "users": 0,
                "users_per_dept": []
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
            message = "The requested callback URL does not " \
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


def get_number_of_requests(token):
    if token.startswith('uclapi-user-'):
        calls = APICall.objects.filter(token__token__exact=token)
    elif token.startswith('uclapi-'):
        calls = APICall.objects.filter(app__api_token__exact=token)
    else:
        return None

    return len(calls)


def number_of_requests(request):
    try:
        token = request.GET["token"]
    except MultiValueDictKeyError:
        response = JsonResponse({
            "ok": False,
            "message": "No token provided"
        })
        response.status_code = 400
        return response

    calls = get_number_of_requests(token)
    if calls is None:
        response = JsonResponse({
            "ok": False,
            "message": "Token is invalid"
        })
        response.status_code = 400
        return response

    return PrettyJsonResponse({
        "ok": True,
        "num": calls,
    })


def get_apps(request):
    if request.method != "GET":
        response = PrettyJsonResponse({
            "success": False,
            "error": "Request is not of method GET"
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

    user = get_user_by_id(user_id)

    user_meta = {
        "name": user.full_name,
        "cn": user.cn,
        "department": user.department,
        "intranet_groups": user.raw_intranet_groups,
        "apps": []
    }

    user_apps = App.objects.filter(user=user, deleted=False)

    s = Scopes()

    for app in user_apps:
        user_meta["apps"].append({
            "name": app.name,
            "id": app.id,
            "token": app.api_token,
            "created": app.created,
            "updated": app.last_updated,
            "oauth": {
                "client_id": app.client_id,
                "client_secret": app.client_secret,
                "callback_url": app.callback_url,
                "scopes": s.scope_dict_all(app.scope.scope_number)
            },
            "webhook": {
                "verification_secret": app.webhook.verification_secret,
                "url": app.webhook.url,
                "siteid": app.webhook.siteid,
                "roomid": app.webhook.roomid,
                "contact": app.webhook.contact
            },
            "analytics": {
                "requests": get_number_of_requests(app.api_token),
                "remaining_quota": get_quota_remaining(app.api_token),
                "users": get_users_per_app(app.api_token),
                "users_per_dept": get_users_per_app_per_dept(app.api_token)
            }
        })

    return PrettyJsonResponse(user_meta)


def get_quota_remaining(token):
    r = redis.Redis(host=REDIS_UCLAPI_HOST)

    if token.startswith('uclapi-user-'):
        Otoken = OAuthToken.objects.filter(token__exact=token).first()
        if Otoken is None:
            return None

        cache_key = "oauth:" + Otoken.user.email
        limit = Otoken.user.oauth_quota

    elif token.startswith('uclapi-'):
        app = App.objects.filter(api_token__exact=token).first()
        if app is None:
            return None

        cache_key = app.user.email
        limit = app.user.dev_quota

    else:
        return None

    count_data = r.get(cache_key)

    if count_data:
        count_data = int(r.get(cache_key))
    else:
        count_data = 0

    return limit - count_data


def quota_remaining(request):
    try:
        token = request.GET["token"]
    except MultiValueDictKeyError:
        response = JsonResponse({
            "ok": False,
            "message": "No token provided"
        })
        response.status_code = 400
        return response

    quota = get_quota_remaining(token)
    if quota is None:
        response = JsonResponse({
            "ok": False,
            "message": "Token is invalid"
        })
        response.status_code = 400
        return response

    return PrettyJsonResponse({
        "ok": True,
        "remaining": quota,
    })


def most_popular_service(request):
    most_common = APICall.objects.values("service").annotate(
        count=Count('service')).order_by("-count")
    most_common = list(most_common)

    return PrettyJsonResponse({
        "ok": True,
        "data": most_common
    })


def most_popular_method(request):
    service = request.GET.get("service", False)
    split_by_service = request.GET.get("split_services", "false")
    split_by_service = False if split_by_service.lower() in [
        "false", "0"] else True

    if service:
        most_common = APICall.objects.filter(service__exact=service)\
            .values("service", "method").annotate(count=Count('method')).order_by("-count")
    else:
        most_common = APICall.objects\
            .values("service", "method").annotate(count=Count('method')).order_by("-count")

    if not split_by_service:
        t_most_common_counter = {}
        for m in most_common:
            if m["method"].split("/")[0] in t_most_common_counter:
                t_most_common_counter[m["method"].split("/")[0]] += m["count"]
            else:
                t_most_common_counter[m["method"].split("/")[0]] = m["count"]
        print(t_most_common_counter)

        most_common = [{"method": method, "count": count}
                       for method, count in t_most_common_counter.items()]
    else:
        temp_most_common_aggregate = {}
        for method in most_common:
            if method["service"] in temp_most_common_aggregate:
                temp_most_common_aggregate[method["service"]].append({
                    "method": method["method"],
                    "count": method["count"]
                })
            else:
                temp_most_common_aggregate[method["service"]] = [{
                    "method": method["method"],
                    "count": method["count"]
                }]
        most_common = temp_most_common_aggregate

    return PrettyJsonResponse({
        "ok": True,
        "data": most_common
    })


def get_users_per_app(token, start=None, end=None):
    if start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        users = OAuthToken.objects.filter(creation_date__gte=start_date,
                                          creation_date__lte=end_date,
                                          app__api_token__exact=token)
    else:
        users = OAuthToken.objects.filter(app__api_token__exact=token)

    return len(users)


def users_per_app(request):
    try:
        token = request.GET["token"]
    except MultiValueDictKeyError:
        response = JsonResponse({
            "ok": False,
            "message": "No token provided"
        })
        response.status_code = 400
        return response

    try:
        start = request.GET["start_date"]
        end = request.GET["end_date"]
        users_count = get_users_per_app(token, start, end)
    except MultiValueDictKeyError:
        users_count = get_users_per_app(token)

    return PrettyJsonResponse({
        "ok": True,
        "users": users_count
    })


def get_users_per_app_per_dept(token):
    users = User.objects.filter(oauthtoken__app__api_token__exact=token)\
        .values("department").annotate(count=Count('department'))\
        .order_by("-count")
    return list(users)


def users_per_app_by_dept(request):
    try:
        token = request.GET["token"]
    except MultiValueDictKeyError:
        response = JsonResponse({
            "ok": False,
            "message": "No token provided"
        })
        response.status_code = 400
        return response

    users = get_users_per_app_per_dept(token)

    return PrettyJsonResponse({
        "ok": True,
        "data": users
    })
