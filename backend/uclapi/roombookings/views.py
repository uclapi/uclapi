from functools import reduce

from os import path

from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q

from .helpers import (PrettyJsonResponse, _create_page_token,
                      _get_paginated_bookings, _parse_datetime,
                      _return_json_bookings, _serialize_equipment,
                      _serialize_rooms, _filter_for_free_rooms, _round_date)
from .models import BookingA, BookingB, Equipment, Lock, Room

from common.decorators import uclapi_protected_endpoint


@api_view(['GET'])
@uclapi_protected_endpoint()
def get_rooms(request, *args, **kwargs):
    # add them to iterables so can be filtered without if-else
    request_params = {}

    request_params['roomid'] = request.GET.get('roomid')
    request_params['siteid'] = request.GET.get('siteid')
    request_params['roomname__contains'] = request.GET.get('roomname')
    request_params['sitename__contains'] = request.GET.get('sitename')
    request_params['category'] = request.GET.get('category')
    request_params['roomclass'] = request.GET.get('classification')
    request_params['capacity__gte'] = request.GET.get('capacity')
    request_params['automated'] = request.GET.get('automated')

    # Get available rooms:
    # - Filtered by this academic year only
    # - Anything centrally bookable
    # - All ICH rooms (Site IDs 238 and 240)
    all_rooms = Room.objects.using("roombookings").filter(
        Q(setid=settings.ROOMBOOKINGS_SETID),
        Q(bookabletype='CB') | Q(siteid="238") | Q(siteid="240")
    )

    # no filters provided, return all rooms serialised
    if not reduce(lambda x, y: x or y, request_params.values()):
        return PrettyJsonResponse({
            "ok": True,
            "rooms": _serialize_rooms(all_rooms)
        }, rate_limiting_data=kwargs)

    request_params = dict((k, v) for k, v in request_params.items() if v)

    filtered_rooms = all_rooms.filter(**request_params)

    return PrettyJsonResponse({
        "ok": True,
        "rooms": _serialize_rooms(filtered_rooms)
    }, rate_limiting_data=kwargs)


@api_view(['GET'])
@uclapi_protected_endpoint()
def get_bookings(request, *args, **kwargs):
    # if page_token exists, dont look for query
    page_token = request.GET.get('page_token')
    if page_token:
        bookings = _get_paginated_bookings(page_token)
        return _return_json_bookings(bookings, rate_limiting_data=kwargs)

    # query params
    request_params = {}

    # non functional filters
    request_params['roomid'] = request.GET.get('roomid')
    # TODO: building?
    request_params['siteid'] = request.GET.get('siteid')
    request_params['roomname'] = request.GET.get('roomname')
    request_params['descrip'] = request.GET.get('description')
    request_params['condisplayname__contains'] = request.GET.get('contact')
    request_params['startdatetime'] = request.GET.get('date')
    # 20 is the default number of bookings per page

    results_per_page = request.GET.get('results_per_page') or 1000

    try:
        results_per_page = int(results_per_page)
        results_per_page = results_per_page if results_per_page > 0 else 1000
    except ValueError:
        return PrettyJsonResponse({
            "ok": False,
            "error": "results_per_page should be an integer"
        }, rate_limiting_data=kwargs)

    results_per_page = results_per_page if results_per_page < 1000 else 1000

    # functional filters
    request_params['startdatetime__gte'] = request.GET.get('start_datetime')
    request_params['finishdatetime__lte'] = request.GET.get('end_datetime')

    is_parsed = True

    if any([
            request_params['startdatetime__gte'],
            request_params['finishdatetime__lte'],
            request_params['startdatetime']
            ]):
        start, end, is_parsed = _parse_datetime(                    # returned
                request_params['startdatetime__gte'],
                request_params['finishdatetime__lte'],
                request_params['startdatetime']
            )
        request_params["startdatetime__gte"] = start
        request_params["finishdatetime__lte"] = end
    # ignore the date since its already parsed
    request_params.pop("startdatetime")

    if not is_parsed:
        return PrettyJsonResponse({
            "ok": False,
            "error": "date/time isn't formatted as suggested in the docs"
        }, rate_limiting_data=kwargs)

    # filter the query dict
    request_params = dict((k, v) for k, v in request_params.items() if v)

    # create a database entry for token
    page_token = _create_page_token(request_params, results_per_page)

    # first page
    bookings = _get_paginated_bookings(page_token)

    lock = Lock.objects.all()[0]
    curr = BookingA if not lock.bookingA else BookingB

    bookings["count"] = curr.objects.filter(**request_params).count()
    response = _return_json_bookings(bookings, rate_limiting_data=kwargs)
    if path.exists("time.txt"):
        with open("time.txt") as file:
            response["Expires"] = file.read()
    return response


@api_view(['GET'])
@uclapi_protected_endpoint()
def get_equipment(request, *args, **kwargs):
    roomid = request.GET.get("roomid")
    siteid = request.GET.get("siteid")

    if not roomid:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "No roomid supplied"
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    if not siteid:
        response = PrettyJsonResponse({
            "ok": False,
            "error": "No siteid supplied"
        }, rate_limiting_data=kwargs)
        response.status_code = 400
        return response

    equipment = Equipment.objects.using("roombookings").filter(
        setid=settings.ROOMBOOKINGS_SETID,
        roomid=roomid,
        siteid=siteid
    )
    return PrettyJsonResponse({
        "ok": True,
        "equipment": _serialize_equipment(equipment)
    }, rate_limiting_data=kwargs)


@api_view(['GET'])
@uclapi_protected_endpoint()
def get_free_rooms(request, *args, **kwargs):
    request_params = {}
    request_params['startdatetime__gte'] = request.GET.get('start_datetime')
    request_params['finishdatetime__lte'] = request.GET.get('end_datetime')

    if (
        not request_params['startdatetime__gte'] or
        not request_params['finishdatetime__lte']
    ):
        return PrettyJsonResponse({
            "ok": False,
            "error": "start_datetime or end_datetime not provided"
        }, rate_limiting_data=kwargs)

    is_parsed = True

    start, end, is_parsed = _parse_datetime(
        request_params['startdatetime__gte'],
        request_params['finishdatetime__lte'],
        None
    )

    if not is_parsed:
        return PrettyJsonResponse({
            "ok": False,
            "error": "date/time isn't formatted as suggested in the docs"
        }, rate_limiting_data=kwargs)

    # Rounding down start date to start of day
    request_params["startdatetime__gte"] = _round_date(start)

    # Rounding up end date to start of next day
    request_params["finishdatetime__lte"] = _round_date(end, up=True)

    # Pagination Logic
    # maxing out results_per_page to get all the bookings in one page
    results_per_page = 100000
    request_params = {k: v for k, v in request_params.items() if v}
    page_token = _create_page_token(request_params, results_per_page)

    # All bookings in the given time period
    bookings = _get_paginated_bookings(page_token)["bookings"]

    # Get available rooms:
    # - Filtered by this academic year only
    # - Anything centrally bookable
    # - All ICH rooms (Site IDs 238 and 240)
    all_rooms = Room.objects.using("roombookings").filter(
        Q(setid=settings.ROOMBOOKINGS_SETID),
        Q(bookabletype='CB') | Q(siteid="238") | Q(siteid="240")
    )
    all_rooms = _serialize_rooms(all_rooms)

    free_rooms = _filter_for_free_rooms(all_rooms, bookings, start, end)

    return PrettyJsonResponse({
        "ok": True,
        "count": len(free_rooms),
        "free_rooms": free_rooms
    }, rate_limiting_data=kwargs)
