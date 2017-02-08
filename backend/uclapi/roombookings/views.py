from functools import reduce

from django.http import JsonResponse
from rest_framework.decorators import api_view
import datetime
from django.core.exceptions import FieldError
from .models import Booking, Room
from .token_auth import does_token_exist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .helpers import _serialize_rooms

import json
import base64


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

    filtered_rooms = all_rooms.filter(**request_params)

    return JsonResponse({
        "ok": True,
        "rooms": _serialize_rooms(filtered_rooms)
    })


@api_view(['GET'])
@does_token_exist
def get_bookings(request):
    # query params
    request_params = {}

    # non functional filters
    request_params['room_id'] = request.GET.get('room_id')
    # TODO: building?
    request_params['site_id'] = request.GET.get('site_id')
    request_params['description'] = request.GET.get('description')
    request_params['contact'] = request.GET.get('contact')
    request_params['date'] = request.GET.get('date')
    # 20 is the default number of bookings per page
    pagination = request.GET.get('pagination') or 20
    pagination = pagination if pagination < 100 else 100

    # functional filters
    request_params['start_time__gte'] = request.GET.get('start_time')
    request_params['end_time__lte'] = request.GET.get('end_time')

    if any([start_time, end_time, request_params['date']]):
        start_time, end_time, request_params['date'], is_parsed = (
            _parse_datetime(
                request_params['start_time__gte'],
                request_params['end_time__lte'],
                request_params['date']
            )
        )

    if not is_parsed:
        return JsonResponse({
            "error": "date/time isn't formatted as suggested in the docs"
        })

    # first page
    bookings = _paginated_result(request_params, 1, pagination)

    return JsonResponse(bookings)


@api_view(['GET'])
@does_token_exist
def paginated_result(request):
    try:
        query = request.GET.get("query")
        page_number = int(request.GET.get("page_number"))
        pagination = int(request.GET.get("paginations"))
    except KeyError:
        return JsonResponse({
            "error": "paginated view didn't get required parameters"
        })
    except TypeError:
        return JsonResponse({
            "error": "pagination and page number should be an int"
        })

    try:
        query = json.loads(base64.b64decode(query).decode())
    except Exception as e:
        print(e)
        return JsonResponse({
            "error": "couldn't decode the query"
        })

    bookings = _paginated_result(query, page_number, pagination)

    return JsonResponse(bookings)


def _paginated_result(query, page_number, pagination):
    try:
        all_bookings = Booking.objects.using('roombookings').filter(**query)
    except FieldError:
        return {
            "error": "something wrong with encoded query params"
        }

    paginator = Paginator(all_bookings, pagination)

    try:
        bookings = paginator.page(page_number)
    except PageNotAnInteger:
        # give first page
        bookings = paginator.page(1)
    except EmptyPage:
        # return last page
        bookings = paginator.page(paginator.num_pages)

    serialized_bookings = _serialize_bookings(bookings)

    next_url = ""

    if page_number < paginator.num_pages:
        next_url = _construct_next_url(page_number + 1, query, pagination)

    return {
        "bookings": serialized_bookings,
        "next_page": next_url
    }


def _construct_next_url(page_number, query, pagination):
    base_url = "https://uclapi.com/v0/roombookings/bookings.pagination?"

    # base64 encode the query and send it with url
    query = json.dumps(query)
    query = base64.b64encode(query.encode('utf-8'))

    params = (
        "query=" + query + "&page_number=" + str(page_number) +
        "&pagination=" + str(pagination)
    )

    return base_url + params


def _parse_datetime(start_time, end_time, search_date):
    try:
        if start_time:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()

        if end_time:
            end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

        if search_date:
            search_date = datetime.datetime.strptime(
                                        search_date, "%Y%m%d").date()
    except Exception as e:
        print(e)
        return -1, -1, -1, False

    return start_time, end_time, search_date, True


def _serialize_bookings(bookings):
    ret_bookings = []

    for bk in bookings:
        ret_bookings.append({
            "room": bk.room.name,
            "site_id": bk.room.site_id,
            "description": bk.description,
            "start_time": bk.start_time,
            "end_time": bk.end_time,
            "contact": bk.contact,
            "booking_id": bk.id
        })

    return ret_bookings
