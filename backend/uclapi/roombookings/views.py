from functools import reduce

from django.http import JsonResponse
from rest_framework.decorators import api_view
import datetime
from .models import Room
from .token_auth import does_token_exist

from .helpers import _parse_datetime, _serialize_rooms, \
    _get_paginated_bookings, _create_page_token


@api_view(['GET'])
@does_token_exist
def get_rooms(request):
    # add them to iterables so can be filtered without if-else
    request_params = {}

    request_params['roomid'] = request.GET.get('roomid')
    request_params['siteid'] = request.GET.get('siteid')
    request_params['name'] = request.GET.get('name')
    request_params['category'] = request.GET.get('category')
    request_params['classification'] = request.GET.get('classification')
    request_params['campusid'] = request.GET.get('campusid')
    request_params['capacity'] = request.GET.get('capacity')

    # webview available rooms
    all_rooms = Room.objects.using("roombookings").filter(
            setid='LIVE-16-17',
            type='CB'
        )

    # no filters provided, return all rooms serialised
    if not reduce(lambda x, y: x or y, request_params.values()):
        return JsonResponse({
            "ok": True,
            "rooms": _serialize_rooms(all_rooms)
        })

    request_params = dict((k, v) for k, v in request_params.items() if v)

    filtered_rooms = all_rooms.filter(**request_params)

    return JsonResponse({
        "ok": True,
        "rooms": _serialize_rooms(filtered_rooms)
    })


@api_view(['GET'])
@does_token_exist
def get_bookings(request):

    # if page_token exists, dont look for query
    page_token = request.GET.get('page_token')
    if page_token:
        bookings = _get_paginated_bookings(page_token)
        return JsonResponse({
            "ok": "error" not in bookings,
            "bookings": bookings
        })

    # query params
    request_params = {}

    # non functional filters
    request_params['room_id'] = request.GET.get('room_id')
    # TODO: building?
    request_params['siteid'] = request.GET.get('site_id')
    request_params['description'] = request.GET.get('description')
    request_params['contactname__contains'] = request.GET.get('contact')
    request_params['startdatetime'] = request.GET.get('date')
    # 20 is the default number of bookings per page

    pagination = request.GET.get('pagination') or 20

    try:
        pagination = int(pagination)
    except ValueError:
        return JsonResponse({
            "ok": False,
            "error": "Pagination should be an integer"
        })

    pagination = pagination if pagination < 100 else 100

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
    print(request_params)
    if not is_parsed:
        return JsonResponse({
            "ok": False,
            "error": "date/time isn't formatted as suggested in the docs"
        })

    # filter the query dict
    request_params = dict((k, v) for k, v in request_params.items() if v)
    # create a database entry for token
    page_token = _create_page_token(request_params, pagination)

    # first page
    bookings = _get_paginated_bookings(page_token)
    print(request_params)
    return JsonResponse({
        "ok": "error" not in bookings,
        "bookings": bookings
    })
