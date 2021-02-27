import os
from typing import Optional

import redis

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.serializers import Serializer
import requests

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST

from .serializers import LibCalLocationGETSerializer, LibCalFormGETSerializer


def _libcal_request_forwarder(url: str, request: Request, serializer: Serializer, key: str, **kwargs) -> JsonResponse:
    """
    Forwards a request to LibCal for a given URL.

    This method implements all the boiler plate needed to proxy a request from
    the client to LibCal and present the response in UCL API style.

    :param url: The URL path to send a request to (e.g. /space/locations)
    :param request: The client's request
    :param key: The key that holds the LibCal JSON response (if the response is HTTP 200).
    :return: A JSON Response.

    """
    r: redis.Redis = redis.Redis(
        host=REDIS_UCLAPI_HOST,
        charset="utf-8",
        decode_responses=True
    )
    # Get OAuth token needed to proxy request
    token: Optional[str] = r.get("libcal:token")
    if not token:
        uclapi_response = JsonResponse({
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }, custom_header_data=kwargs)
        uclapi_response.status_code = 500
        return uclapi_response

    headers: dict = {
        "Authorization": f"Bearer {token}"
    }
    if not serializer.is_valid():
        uclapi_response = JsonResponse({
            "ok": False,
            "error": "Query parameters are invalid",
            **serializer.errors
        }, custom_header_data=kwargs)
        uclapi_response.status_code = 400
        return uclapi_response

    # NOTE: A serializer may set the "ids" field. This field, if set, is appended to the URL instead of sent as a GET
    # parameter.
    ids = serializer.validated_data.pop("ids", "")
    libcal_response: requests.Response = requests.get(
        url=f'{os.environ["LIBCAL_BASE_URL"]}{url}{"/" + ids if ids else ""}',
        headers=headers,
        params=serializer.validated_data
    )
    if libcal_response.status_code == 200:
        uclapi_response = JsonResponse({
            "ok": True,
            key: libcal_response.json()
        }, custom_header_data=kwargs)
        uclapi_response.status_code = libcal_response.status_code
        return uclapi_response
    elif libcal_response.status_code == 401:
        # For some reason our OAuth token isn't accepted by LibCal...
        # The fact that we're unauthorised is "our" issue so don't confuse the
        # client with this information and instead send back a 500.
        uclapi_response = JsonResponse({
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }, custom_header_data=kwargs)
        uclapi_response.status_code = 500
        return uclapi_response
    else:
        uclapi_response = JsonResponse({
            "ok": False,
            "error": libcal_response.json()["error"] if "error" in libcal_response.json() else libcal_response.json()
        }, custom_header_data=kwargs)
        return uclapi_response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_locations(request, *args, **kwargs):
    """Returns a list of all locations."""
    return _libcal_request_forwarder(
        "/1.1/space/locations",
        request,
        LibCalLocationGETSerializer(data=request.query_params),
        'locations',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_form(request, *args, **kwargs):
    """Returns a form or a list of forms"""
    return _libcal_request_forwarder(
        "/1.1/space/form",
        request,
        LibCalFormGETSerializer(data=request.query_params),
        'forms',
        **kwargs
    )
