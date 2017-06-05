from dashboard.models import App, TemporaryToken
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST
from .helpers import PrettyJsonResponse as JsonResponse, how_many_seconds_until_midnight

import datetime
import keen
import re
import redis

def does_token_exist(view_func):

    def wrapped(request, *args, **kwargs):
        # First check if using a TemporaryToken
        temp_token_param = request.GET.get("temp_token")
        if temp_token_param:
            try:
                temp_token = TemporaryToken.objects.get(
                    api_token=temp_token_param
                )
            except ObjectDoesNotExist:
                response = JsonResponse({
                    "ok": False,
                    "error": "Invalid temporary token"
                })
                response.status_code = 400
                return response

            # Check if TemporaryToken is still valid
            existed = datetime.datetime.now() - temp_token.created

            if temp_token.uses > 10 or existed.seconds > 300:
                temp_token.delete()  # Delete expired token
                response = JsonResponse({
                    "ok": False,
                    "error": "Temporary token expired"
                })
                response.status_code = 400
                return response

            temp_token.uses += 1
            temp_token.save()
            return view_func(request, *args, **kwargs)

        # Else verify normal token
        token = request.GET.get("token")

        if not token:
            response = JsonResponse({
                "ok": False,
                "error": "No token provided"
            })
            response.status_code = 400
            return response

        try:
            App.objects.get(api_token=token)
        except ObjectDoesNotExist:
            response = JsonResponse({
                "ok": False,
                "error": "Token does not exist"
            })
            response.status_code = 400
            return response

        return view_func(request, *args, **kwargs)

    return wrapped


def log_api_call(view_func):
    def wrapped(request, *args, **kwargs):
        service = request.path.split("/")[1]
        method = request.path.split("/")[2]

        headers = request.META
        version_headers = {}
        regex = re.compile("^HTTP_UCLAPI_.*_VERSION$")
        for header in headers:
            if regex.match(header):
                version_headers[header] = headers[header]

        queryparams = dict(request.GET)

        # Check if temp token
        temp_token_param = request.GET.get("temp_token")

        if temp_token_param:
            parameters = {
                "service": service,
                "method": method,
                "version-headers": version_headers,
                "queryparams": queryparams,
                "temp_token": True
            }

            keen.add_event("apicall", parameters)

            return view_func(request, *args, **kwargs)

        token = request.GET["token"]

        user = App.objects.get(api_token=token).user

        parameters = {
            "userid": user.id,
            "email": user.email,
            "name": user.given_name,
            "service": service,
            "method": method,
            "version-headers": version_headers,
            "queryparams": queryparams
        }

        keen.add_event("apicall", parameters)

        return view_func(request, *args, **kwargs)

    return wrapped

def throttle(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET.get("token")
        cache_key = App.objects.get(api_token=token).user.email

        r = redis.StrictRedis(host=REDIS_UCLAPI_HOST)
        count = r.get(cache_key)

        if count is None:
            # set the value to 1 & expiry
            r.set(cache_key, 1, how_many_seconds_until_midnight())
            
            return view_func(request, *args, **kwargs)
        else:
            count = int(count)
            if count > 10000:
                response = JsonResponse({
                    "ok": False,
                    "error": "You have been throttled. Please try again in {} seconds.".format(how_many_seconds_until_midnight())
                })
                response.status_code = 429
                response['Retry-After'] = how_many_seconds_until_midnight()
                return response
            else:
                r.incr(cache_key)
                return view_func(request, *args, **kwargs)

    return wrapped