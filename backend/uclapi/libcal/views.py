import json
import os
from typing import Optional

import redis

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.serializers import Serializer
import requests

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse
from uclapi.settings import REDIS_UCLAPI_HOST

from .serializers import (
    LibCalLocationGETSerializer,
    LibCalIdSerializer,
    LibCalIdListSerializer,
    LibCalCategoryGETSerializer,
    LibCalItemGETSerializer,
    LibCalNicknameGETSerializer,
    LibCalUtilizationGETSerializer,
    LibCalSeatGETSerializer,
    LibCalSeatsGETSerializer,
    LibCalBookingsGETSerializer,
    LibCalPersonalBookingsGETSerializer,
    LibCalReservationPOSTSerializer,
    LibCalBookingIdListSerializer
)

from .utils import cameliser, underscorer, whitelist_fields


def _libcal_request_forwarder(
    url: str, request: Request, serializer: Serializer, key: str, method: str = 'GET', **kwargs
) -> JsonResponse:
    """
    Forwards a request to LibCal for a given URL.

    This method implements all the boiler plate needed to proxy a request from
    the client to LibCal and present the response in UCL API style.

    :param url: The URL path to send a request to (e.g. /space/locations)
    :param request: The client's request
    :param method: Method to use for the request.
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
            "error": f"{'Query parameters are' if request.method == 'GET' else 'Payload is'} invalid",
            **serializer.errors
        }, custom_header_data=kwargs)
        uclapi_response.status_code = 400
        return uclapi_response

    # NOTE: A serializer may set the "ids" field. This field, if set, is appended to the URL instead of sent as a GET
    # parameter.
    ids = str(serializer.validated_data.pop("ids", ""))
    if method == 'GET':
        libcal_response: requests.Response = requests.get(
            url=f'{os.environ["LIBCAL_BASE_URL"]}{url}{"/" + ids if ids else ""}',
            headers=headers,
            params=serializer.validated_data
        )
    else:  # Assume request.method == 'POST'
        libcal_response: requests.Response = requests.post(
            url=f'{os.environ["LIBCAL_BASE_URL"]}{url}{"/" + ids if ids else ""}',
            headers=headers,
            # /1.1/space/reserve expects JSON payload
            data=JSONRenderer().render(serializer.validated_data)
        )

    if libcal_response.status_code == 200:
        uclapi_response = JsonResponse({
            "ok": True,
            key: underscorer(libcal_response.json())
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
        try:
            data = libcal_response.json()
        except json.JSONDecodeError:
            uclapi_response = JsonResponse({
                "ok": False,
                "error": "LibCal endpoint did not return a JSON response."
            }, custom_header_data=kwargs)
            uclapi_response.status_code = 500
            return uclapi_response

        uclapi_response = JsonResponse({
            "ok": False,
            "error": data["error"] if "error" in data else underscorer(data)
        }, custom_header_data=kwargs)
        return uclapi_response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_locations(request, *args, **kwargs):
    """Returns a list of all locations."""
    return _libcal_request_forwarder(
        "/1.1/space/locations",
        request,
        LibCalLocationGETSerializer(data=cameliser(request.query_params)),
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
        LibCalIdListSerializer(data=cameliser(request.query_params)),
        'forms',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_question(request, *args, **kwargs):
    """Returns a question or a list of questions"""
    return _libcal_request_forwarder(
        "/1.1/space/question",
        request,
        LibCalIdListSerializer(data=cameliser(request.query_params)),
        'questions',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_categories(request, *args, **kwargs):
    """Returns a list of categories given a location ID(s)"""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/1.1/space/categories",
        request,
        LibCalIdListSerializer(data=cameliser(request.query_params)),
        'categories',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_category(request, *args, **kwargs):
    """Returns a category or a list of categories"""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/1.1/space/category",
        request,
        LibCalCategoryGETSerializer(data=cameliser(request.query_params)),
        'categories',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_item(request, *args, **kwargs):
    """Returns a item or a list of items"""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/1.1/space/item",
        request,
        LibCalItemGETSerializer(data=cameliser(request.query_params)),
        'items',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_nickname(request, *args, **kwargs):
    """Returns the nicknames of a category or a list of categories"""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/1.1/space/nickname",
        request,
        LibCalNicknameGETSerializer(data=cameliser(request.query_params)),
        'nicknames',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_utilization(request, *args, **kwargs):
    """Returns the utilization of a given location"""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/api/1.1/space/utilization",
        request,
        LibCalUtilizationGETSerializer(data=cameliser(request.query_params)),
        'data',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_seat(request, *args, **kwargs):
    """Returns a seat."""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/api/1.1/space/seat",
        request,
        LibCalSeatGETSerializer(data=cameliser(request.query_params)),
        'seat',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_seats(request, *args, **kwargs):
    """Returns seats for a given location."""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/api/1.1/space/seats",
        request,
        LibCalSeatsGETSerializer(data=cameliser(request.query_params, special=False)),
        'seats',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_zone(request, *args, **kwargs):
    """Returns a zone."""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/api/1.1/space/zone",
        request,
        LibCalIdSerializer(data=cameliser(request.query_params)),
        'zone',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_zones(request, *args, **kwargs):
    """Returns zones for a given location."""
    # TODO: note in docs an invalid ID will have different key/values!!
    return _libcal_request_forwarder(
        "/api/1.1/space/zones",
        request,
        LibCalIdSerializer(data=cameliser(request.query_params)),
        'zones',
        **kwargs
    )


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False, last_modified_redis_key=None)
def get_bookings(request, *args, **kwargs):
    """Returns bookings based on parameters (if any) given."""
    serializer = LibCalBookingsGETSerializer(
        data=cameliser(request.query_params))
    booking_response = _libcal_request_forwarder(
        "/1.1/space/bookings", request, serializer, 'data', **kwargs)
    data = json.loads(booking_response.content.decode('utf-8'))
    if "data" in data:
        data["bookings"] = data.pop("data")
        if isinstance(data["bookings"], list):
            for i in range(len(data["bookings"])):
                # Ensure we don't leak personal data, only allow the following fields
                allowed_fields = ['eid', 'cid', 'lid', 'from_date', 'to_date', 'created', 'status',
                                  'location_name', 'category_name', 'item_name', 'seat_id', 'seat_name', 'cancelled']
                data['bookings'][i] = whitelist_fields(data['bookings'][i], allowed_fields)
    uclapi_response = JsonResponse(data, custom_header_data=kwargs)
    uclapi_response.status_code = booking_response.status_code
    return uclapi_response


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=True, required_scopes=['libcal_read'], last_modified_redis_key=None)
def get_personal_bookings(request, *args, **kwargs):
    """Returns personal bookings for a user. Requires OAuth permissions"""
    user = kwargs['token'].user
    params = request.query_params.copy()
    # NOTE: serializer will catch if this is empty (default is '').
    params["email"] = user.mail if user.mail else user.email
    return _libcal_request_forwarder(
        "/1.1/space/bookings",
        request,
        LibCalPersonalBookingsGETSerializer(data=cameliser(params)),
        'bookings',
        **kwargs
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@uclapi_protected_endpoint(personal_data=True, required_scopes=['libcal_write'], last_modified_redis_key=None)
def reserve(request, *args, **kwargs):
    """Reserves a space/seat on behalf of a user. Requires OAuth permissions"""
    user = kwargs['token'].user
    # NOTE: serializer will catch if this is empty (default is '').
    request.data["email"] = user.mail if user.mail else user.email
    request.data["fname"] = user.given_name
    request.data["lname"] = user.sn
    print(request.data)
    print(user)
    return _libcal_request_forwarder(
        "/1.1/space/reserve",
        request,
        LibCalReservationPOSTSerializer(data=cameliser(request.data)),
        'bookings',
        'POST',
        **kwargs
    )


@api_view(["POST"])
@uclapi_protected_endpoint(personal_data=True, required_scopes=['libcal_write'], last_modified_redis_key=None)
def cancel(request, *args, **kwargs):
    """Cancels a booking on behalf of a user."""
    # The /1.1/space/cancel endpoint simply accepts a booking ID(s) as a way of cancelling.
    # This format of the ID seems to be r"^cs_\w{8}$" thus allowing an attacker to cancel arbitrary bookings by process
    # of enumeration.
    # We add an additional level of security by checking the personal OAuth token, to check that the app cancelling a
    # booking has permission to delete the booking associated with the user.
    user = kwargs['token'].user
    email = user.mail if user.mail else user.email
    if not email:
        uclapi_response = JsonResponse({
            "ok": False,
            "error": "This booking cannot be cancelled as this user has no valid email address."
        }, custom_header_data=kwargs)
        uclapi_response.status_code = 500
        return uclapi_response

    booking_response = _libcal_request_forwarder(
        "/1.1/space/booking",
        request,
        LibCalBookingIdListSerializer(data=cameliser(request.query_params)),
        'data',
        **kwargs
    )
    data = json.loads(booking_response.content.decode('utf-8'))
    if "data" not in data:
        # An error occured with this request, forward to user.
        return booking_response
    else:
        # Only send the booking IDs to LibCal that correspond to the user
        legit_bids = ''
        for booking in data["data"]:
            if booking["email"] == email:
                legit_bids += booking["book_id"] + ','
        if legit_bids:
            legit_bids = legit_bids[:-1]  # Remove last ','
        else:
            uclapi_response = JsonResponse({
                "ok": False,
                "error": "No bookings matched the IDs provided and so no bookings were deleted"
            }, custom_header_data=kwargs)
            uclapi_response.status_code = 400
            return uclapi_response

    return _libcal_request_forwarder(
        "/1.1/space/cancel",
        request,
        LibCalBookingIdListSerializer(data={'ids': legit_bids}),
        'bookings',
        'POST',
        **kwargs
    )
