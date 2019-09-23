import re

from base64 import b64decode

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from common.helpers import RateLimitHttpResponse as HttpResponse

from rest_framework.decorators import api_view

# from .occupeye import BadOccupEyeRequest, OccupEyeApi
from .occupeye.api import OccupEyeApi
from .occupeye.constants import OccupEyeConstants
from .occupeye.exceptions import BadOccupEyeRequest
from .image_builder import ImageBuilder


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
def get_surveys(request, *args, **kwargs):
    api = OccupEyeApi()
    consts = OccupEyeConstants()

    survey_filter = request.GET.get("survey_filter", "student")
    if survey_filter not in consts.VALID_SURVEY_FILTERS:
        response = JsonResponse({
            "ok": False,
            "error": (
                "The survey filter you provided is invalid. "
                "Valid survey filters are: "
            ) + str(consts.VALID_SURVEY_FILTERS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    response_data = {
        "ok": True,
        "surveys": api.get_surveys(survey_filter)
    }
    return JsonResponse(
        response_data,
        custom_header_data=kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
def get_map_image(request, *args, **kwargs):
    try:
        image_id = request.GET['image_id']
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": "No Image ID provided."
        }, custom_header_data=kwargs)
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
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    image_format = request.GET.get("image_format", "base64")

    if image_format == "raw":
        return HttpResponse(
            content=b64decode(image_b64),
            custom_header_data=kwargs,
            content_type=content_type
        )
    elif image_format == "base64":
        response = JsonResponse({
            "ok": True,
            "content_type": content_type,
            "data": image_b64
        }, custom_header_data=kwargs)
        return response
    else:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You specified a response format that "
                "was not either raw or base64."
            )
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
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

    api = OccupEyeApi()
    try:
        data = api.get_survey_sensors(survey_id)
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
    }, custom_header_data=kwargs)
    return response


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
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
    }, custom_header_data=kwargs)

    return response


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
def get_survey_sensors_summary(request, *args, **kwargs):
    survey_ids = request.GET.get("survey_ids", None)

    survey_filter = request.GET.get("survey_filter", "student")
    consts = OccupEyeConstants()
    if survey_filter not in consts.VALID_SURVEY_FILTERS:
        response = JsonResponse({
            "ok": False,
            "error": (
                "The survey filter you provided is invalid. "
                "Valid survey filters are: "
            ) + str(consts.VALID_SURVEY_FILTERS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    api = OccupEyeApi()
    try:
        data = api.get_survey_sensors_summary(survey_ids, survey_filter)
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": (
                "One or more of the survey_ids you requested is not valid."
            )
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    response = JsonResponse({
        "ok": True,
        "surveys": data
    }, custom_header_data=kwargs)

    return response


@api_view(["GET"])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
def get_historical_time_data(request, *args, **kwargs):
    api = OccupEyeApi()
    consts = OccupEyeConstants()

    survey_ids = request.GET.get("survey_ids", None)
    survey_filter = request.GET.get("survey_filter", "student")
    if survey_filter not in consts.VALID_SURVEY_FILTERS:
        response = JsonResponse({
            "ok": False,
            "error": (
                "The survey filter you provided is invalid. "
                "Valid survey filters are: "
            ) + str(consts.VALID_SURVEY_FILTERS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    try:
        day_count = request.GET["days"]
    except KeyError:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify how many days of historical data "
                "should be returned. Valid options are: "
            ) + str(consts.VALID_HISTORICAL_DATA_DAYS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    if not day_count.isdigit():
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify an integer number of days of "
                "historical days. Valid options are: "
            ) + str(consts.VALID_HISTORICAL_DATA_DAYS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    day_count = int(day_count)

    if day_count not in consts.VALID_HISTORICAL_DATA_DAYS:
        response = JsonResponse({
            "ok": False,
            "error": (
                "You did not specify a valid number of days of "
                "historical days. Valid options are: "
            ) + str(consts.VALID_HISTORICAL_DATA_DAYS)
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    try:
        data = api.get_historical_time_usage_data(
            survey_ids,
            day_count,
            survey_filter
        )
    except BadOccupEyeRequest:
        response = JsonResponse({
            "ok": False,
            "error": (
                "One or more of the survey_ids you requested is not valid."
            )
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    response = JsonResponse({
        "ok": True,
        "surveys": data
    }, custom_header_data=kwargs)

    return response


@api_view(['GET'])
@uclapi_protected_endpoint(
    personal_data=False,
    last_modified_redis_key='Workspaces'
)
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
        }, custom_header_data=kwargs)
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

    image_scale_str = request.GET.get(
        "image_scale",
        "0.02"
    )

    circle_radius_str = request.GET.get(
        "circle_radius",
        "128"
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
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    try:
        image_scale = float(image_scale_str)
    except ValueError:
        response = JsonResponse({
            "ok": False,
            "error": (
                "The scale you specified is not valid. It "
                "must be a floating point number, such as 1 "
                "or 0.02."
            )
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    try:
        circle_radius = float(circle_radius_str)
    except ValueError:
        response = JsonResponse({
            "ok": False,
            "error": (
                "The circle radiuus you specified is not valid. "
                "It must be a floating point number, such as 128 or "
                "100.5."
            )
        }, custom_header_data=kwargs)
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
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    ib.set_colours(
        absent=absent_colour,
        occupied=occupied_colour
    )
    ib.set_circle_radius(
        circle_radius=circle_radius
    )
    ib.set_image_scale(
        image_scale=image_scale
    )
    map_svg = ib.get_live_map()

    response = HttpResponse(
        map_svg,
        content_type="image/svg+xml",
        custom_header_data=kwargs
    )
    response["Content-Length"] = len(map_svg)

    return response
