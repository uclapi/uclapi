from dashboard.models import App
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import keen
import re


def does_token_exist(view_func):
    def wrapped(request, *args, **kwargs):
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
