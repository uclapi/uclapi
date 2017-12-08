from base64 import b64decode

from rest_framework.decorators import api_view

from common.decorators import uclapi_protected_endpoint
from common.helpers import (
    PrettyJsonResponse as JsonResponse,
    RateLimitHttpResponse as HttpResponse
)

from .decorators import occupeye_api_request
from .occupeye import BadOccupEyeRequest


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
@occupeye_api_request()
def get_rooms(request, *args, **kwargs):
    api = kwargs['OccupEyeApi']
    response_data = {
        "ok": True,
        "rooms": api.get_surveys()
    }
    return JsonResponse(
        response_data,
        rate_limiting_data=kwargs
    )

@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
@occupeye_api_request()
def get_image(request, *args, **kwargs):
    api = kwargs['OccupEyeApi']
    try:
        image_id = request.GET['image_id']
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "No Image ID provided."
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    try:
        (
            image_b64,
            content_type
        ) = api.get_image(image_id)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": "Either the Image ID you requested does "
                     "not exist, or an internal error occured "
                     "that prevented it from being retrieved."
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    image_format = request.GET.get("image_format")
    if not image_format:
        image_format = "base64"

    if image_format == "raw":
        return HttpResponse(
            content=b64decode(image_b64),
            rate_limiting_data=kwargs,
            content_type=content_type
        )
    elif image_format == "base64":
        response = JsonResponse({
            "ok": True,
            "content_type": content_type,
            "data": image_b64
        }, rate_limiting_data=kwargs)
        return response
    else:
        response = JsonResponse({
            "ok": False,
            "error": "You specified a response format that "
                     "was not either raw or base64."
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response
