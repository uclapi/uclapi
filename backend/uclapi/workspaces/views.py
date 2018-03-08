import re

from base64 import b64decode

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from common.helpers import RateLimitHttpResponse as HttpResponse

from rest_framework.decorators import api_view

from .occupeye import BadOccupEyeRequest, OccupEyeApi
from .image_builder import ImageBuilder

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
def get_map_image(request, *args, **kwargs):
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
                "The image with the ID you requested "
                "does not exist."
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


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_historical_time_data(request, *args, **kwargs):
    api = OccupEyeApi()
    survey_ids = request.GET.get("survey_ids", None)
    try:
        day_count = request.GET["days"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify how many days of historical data "
                "should be returned. Valid options are: "
            ) + str(api.VALID_HISTORICAL_DATA_DAYS)
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    if not day_count.isdigit():
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify an integer number of days of "
                "historical days. Valid options are: "
            ) + str(api.VALID_HISTORICAL_DATA_DAYS)
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    day_count = int(day_count)

    if day_count not in api.VALID_HISTORICAL_DATA_DAYS:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify a valid number of days of "
                "historical days. Valid options are: "
            ) + str(api.VALID_HISTORICAL_DATA_DAYS)
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    try:
        data = api.get_historical_time_usage_data(survey_ids, day_count)
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


@api_view(['GET'])
@uclapi_protected_endpoint(personal_data=False)
def get_live_map(request, *args, **kwargs):
    try:
        survey_id = request.GET["survey_id"]
        map_id = request.GET["map_id"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You must provide a Survey ID and a Map ID "
                "to get a live sensor status image."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    # Thank you Stack Overflow
    # https://stackoverflow.com/a/1636354/5297057
    colour_pattern = re.compile(
        "^#(?:[0-9a-fA-F]{3}){1,2}$"
    )

    absent_colour = request.GET.get(
        "absent_colour",
        "#ABE00C"
    )

    occupied_colour = request.GET.get(
        "occupied_colour",
        "#FFC90E"
    )

    if not re.match(colour_pattern, absent_colour) or \
       not re.match(colour_pattern, occupied_colour):
        response = JsonResponse({
            "ok": False,
            "error": (
                "The custom colours you specfied did not match "
                "the format of HTML hex colours. Colours must "
                "either be in the format #ABC or #ABCDEF."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    try:
        ib = ImageBuilder(survey_id, map_id)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": (
                "Either the IDs you sent were not "
                "integers, or they do not exist."
            )
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    ib.set_colours(absent_colour, occupied_colour)

    map_svg = ib.get_live_map()

    response = HttpResponse(
        map_svg,
        content_type="image/svg+xml",
        rate_limiting_data=kwargs
    )
    response["Content-Length"] = len(map_svg)

    return response
