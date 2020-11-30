import os
from typing import Tuple, Optional

import redis

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.serializers import Serializer
import requests

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST

from .serializers import LibCalLocationGETSerializer


def _libcal_request_forwarder(url: str, request: Request, serializer: Serializer) -> Tuple[dict, int]:
    """
    Forwards a request to LibCal for a given URL.

    This method implements all the boiler plate needed to proxy a request from
    the client to LibCal and present the response in UCL API style.

    :param url: The URL path to send a request to (e.g. /space/locations)
    :param request: The client's request
    :return: A tuple consisting of the JSON data to return and the status code.

    """
    r: redis.Redis = redis.Redis(
        host=REDIS_UCLAPI_HOST,
        charset="utf-8",
        decode_responses=True
    )
    # Get OAuth token needed to proxy request
    token: Optional[str] = r.get("libcal:token")
    if not token:
        response_data = {
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }
        return response_data, 500

    headers: dict = {
        "Authorization": f"Bearer {token}"
    }
    if not serializer.is_valid():
        response_data = {
            "ok": False,
            "error": "Query parameters are invalid"
        }
        response_data.update(serializer.errors)
        return response_data, 400
    response: requests.Response = requests.get(
        url=os.environ["LIBCAL_BASE_URL"] + url,
        headers=headers,
        params=serializer.validated_data
    )
    if response.status_code == 200:
        response_data = {
            "ok": True,
            "data": response.json()
        }
        return response_data, response.status_code
    elif response.status_code == 401:
        # For some reason our OAuth token isn't accepted by LibCal...
        # The fact that we're unauthorised is "our" issue so don't confuse the
        # client with this information and instead send back a 500.
        response_data = {
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }
        return response_data, 500
    else:
        response_data = {
            "ok": False,
            "error": response.json()["error"] if "error" in response.json() else response.json()
        }
        return response_data, response.status_code


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_locations(request, *args, **kwargs):
    """Returns a list of all locations."""
    serializer = LibCalLocationGETSerializer(data=request.query_params)
    data, status_code = _libcal_request_forwarder("/1.1/space/locations", request, serializer)
    if "data" in data:
        data["locations"] = data.pop("data")
    response = JsonResponse(data, custom_header_data=kwargs)
    response.status_code = status_code
    return response
