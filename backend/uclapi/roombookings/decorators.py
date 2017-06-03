from dashboard.models import App, TemporaryToken
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import datetime
import keen
import re


def does_token_exist(view_func):

    def wrapped(request, *args, **kwargs):
        # First check if using a TemporaryToken
        token = request.GET.get("token")
        is_temp_token = None

        try:
            if token.split("-")[1] == "temp":
                is_temp_token = True
        except:
            is_temp_token = False

        if is_temp_token:
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

            if request.path != "roombookings/bookings":
                temp_token.uses += 1
                temp_token.save()
                response = JsonResponse({
                    "ok": False,
                    "error": "Temporary token can only be used for /bookings"
                })
                response.status_code = 400
                return response

            if request.GET.get('page_token'):
                temp_token.uses += 1
                temp_token.save()
                response = JsonResponse({
                    "ok": False,
                    "error": "Temporary token can only return one booking"
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

            request.GET = request.GET.copy()
            request.GET['results_per_page'] = 1

            temp_token.uses += 1
            temp_token.save()
            return view_func(request, *args, **kwargs)

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
