from functools import reduce

from django.http import JsonResponse
from rest_framework.decorators import api_view
import datetime
from .models import Room
from .token_auth import does_token_exist

from .private_methods import _parse_datetime, _serialize_rooms, \
    _paginated_result, _serialize_bookings, _get_paginated_bookings, \
    _create_page_token


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
    print(all_rooms)
    # no filters provided, return all rooms serialised
    if not reduce(lambda x, y: x or y, request_params.values()):
        return JsonResponse(_serialize_rooms(all_rooms), safe=False)

    request_params = dict((k, v) for k, v in request_params.items() if v)

    filtered_rooms = all_rooms.filter(**request_params)

    return JsonResponse(_serialize_rooms(filtered_rooms), safe=False)


@api_view(['GET'])
@does_token_exist
def get_bookings(request):

    # if page_token exists, dont look for query
    page_token = request.GET.get('page_token')
    if page_token:
        bookings = _get_paginated_bookings(page_token)
        return JsonResponse(bookings)

    # query params
    request_params = {}

    # non functional filters
    request_params['room_id'] = request.GET.get('room_id')
    # TODO: building?
    request_params['siteid'] = request.GET.get('site_id')
    request_params['description'] = request.GET.get('description')
    request_params['contact__contains'] = request.GET.get('contact')
    request_params['startdatetime'] = request.GET.get('date')
    # 20 is the default number of bookings per page
    pagination = request.GET.get('pagination') or 20
    pagination = pagination if pagination < 100 else 100

    # functional filters
    request_params['starttime__gte'] = request.GET.get('start_time')
    request_params['finishtime__lte'] = request.GET.get('end_time')

    is_parsed = True

    if any([
            request_params['starttime__gte'],
            request_params['finishtime__lte'],
            request_params['startdatetime']
            ]):
        start_time, end_time, request_params['date'], is_parsed = (
            _parse_datetime(
                request_params['starttime__gte'],
                request_params['finishtime__lte'],
                request_params['startdatetime']
            )
        )

    if not is_parsed:
        return JsonResponse({
            "error": "date/time isn't formatted as suggested in the docs"
        })

    # filter the query dict
    request_params = dict((k, v) for k, v in request_params.items() if v)

    # create a database entry for token
    page_token = _create_page_token(request_params, pagination)

    # first page
    bookings = _get_paginated_bookings(page_token)

    return JsonResponse(bookings)
