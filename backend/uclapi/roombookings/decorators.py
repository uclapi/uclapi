import keen
import re
import redis
from django.core.exceptions import ObjectDoesNotExist

from dashboard.models import App
from uclapi.settings import REDIS_UCLAPI_HOST

from .helpers import PrettyJsonResponse
from .helpers import how_many_seconds_until_midnight


def does_token_exist(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET.get("token")

        if not token:
            response = PrettyJsonResponse({
                "ok": False,
                "error": "No token provided"
            })
            response.status_code = 400
            return response

        try:
            App.objects.get(api_token=token)
        except ObjectDoesNotExist:
            response = PrettyJsonResponse({
                "ok": False,
                "error": "Token does not exist"
            })
            response.status_code = 400
            return response

        return view_func(request, *args, **kwargs)
    return wrapped


def log_api_call(view_func):
    def wrapped(request, *args, **kwargs):
        token = request.GET["token"]

        user = App.objects.get(api_token=token).user

        service = request.path.split("/")[1]
        method = request.path.split("/")[2]

        headers = request.META
        version_headers = {}
        regex = re.compile("^HTTP_UCLAPI_.*_VERSION$")
        for header in headers:
            if regex.match(header):
                version_headers[header] = headers[header]

        queryparams = dict(request.GET)

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
                response = PrettyJsonResponse({
                    "ok": False,
                    "error": "You have been throttled. "
                             "Please try again in {} seconds."
                             .format(how_many_seconds_until_midnight())
                })
                response.status_code = 429
                response['Retry-After'] = how_many_seconds_until_midnight()
                return response
            else:
                r.incr(cache_key)
                return view_func(request, *args, **kwargs)

    return wrapped
