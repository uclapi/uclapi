from base64 import b64decode

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from common.helpers import RateLimitHttpResponse as HttpResponse
from rest_framework.decorators import api_view

from .occupeye import BadOccupEyeRequest, OccupEyeApi


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_surveys(request, *args, **kwargs):
    api = OccupEyeApi()
    response_data = {
        "ok": True,
        "surveys": api.get_surveys()
    }
    return JsonResponse(
        response_data,
        rate_limiting_data=kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_image(request, *args, **kwargs):
    try:
        image_id = request.GET['image_id']
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "No Image ID provided."
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    api = OccupEyeApi()

    try:
        (
            image_b64,
            content_type
        ) = api.get_image(image_id)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": (
                "Either the Image ID you requested does "
                "not exist, or an internal error occured "
                "that prevented it from being retrieved."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    image_format = request.GET.get("image_format", "base64")

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
            "error": (
                "You specified a response format that "
                "was not either raw or base64."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_survey_sensors(request, *args, **kwargs):
    try:
        survey_id = request.GET["survey_id"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Please specify a survey_id."
        })
        response.status_code = 400
        return response

    # Check if state data should be returned
    try:
        return_states = request.GET["return_states"].lower() == "true"
    except KeyError:
        return_states = False

    api = OccupEyeApi()
    try:
        data = api.get_survey_sensors(
            survey_id,
            return_states=return_states
        )
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": "The survey_id you specified was not valid."
        })
        response.status_code = 400
        return response

    response = JsonResponse({
        "ok": True,
        **data
    })
    return response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_survey_max_timestamp(request, *args, **kwargs):
    try:
        survey_id = request.GET["survey_id"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "Please specify a survey_id."
        })
        response.status_code = 400
        return response

    api = OccupEyeApi()
    try:
        (
            survey_id_int,
            max_timestamp
        ) = api.get_max_survey_timestamp(survey_id)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": "The survey_id you specified was not valid."
        })
        response.status_code = 400
        return response

    response = JsonResponse({
        "ok": True,
        "survey_id": survey_id_int,
        "last_updated": max_timestamp
    }, rate_limiting_data=kwargs)

    return response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_survey_sensors_summary(request, *args, **kwargs):
    survey_ids = request.GET.get("survey_ids", None)
    api = OccupEyeApi()
    try:
        data = api.get_survey_sensors_summary(survey_ids)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": (
                "One or more of the survey_ids you requested is not valid."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    response = JsonResponse({
        "ok": True,
        "surveys": data
    }, rate_limiting_data=kwargs)

    return response
