from functools import reduce

from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
import datetime
from django.core.exceptions import FieldError
from .models import Booking, Room, PageToken
from .token_auth import does_token_exist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    print(all_rooms)
    # no filters provided, return all rooms serialised
    if not reduce(lambda x, y: x or y, request_params.values()):
        return JsonResponse(_serialize_rooms(all_rooms))

    print(request_params)

    filtered_rooms = all_rooms.filter(**request_params)

    return JsonResponse(_serialize_rooms(filtered_rooms))


@api_view(['GET'])
# @does_token_exist
def get_bookings(request):

    # if page_token exists, dont look for query
    page_token = request.POST.get('page_token')
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
    request_params['contact'] = request.GET.get('contact')
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


def _create_page_token(query, pagination):
    page = PageToken(
        pagination=pagination,
        query=json.dumps(query)
    )
    page.save()
    return page.page_token


def _get_paginated_bookings(page_token):
    try:
        page = PageToken.objects.get(page_token=page_token)
    except ObjectDoesNotExist:
        return {
            "error": "Page token does not exist"
        }

    curr_page = page.curr_page
    page.curr_page += 1
    page.save()

    pagination = page.pagination
    query = json.loads(page.query)
    bookings = _paginated_result(query, curr_page + 1, pagination)

    # append the page_token to return json
    bookings["page_token"] = page_token

    return bookings


def _paginated_result(query, page_number, pagination):
    try:
        all_bookings = Booking.objects.using('roombookings').filter(**query)
    except FieldError as e:
        print(e)
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

    return {
        "bookings": serialized_bookings,
    }


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


def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        rooms.append({
            "name": room.name,
            "room_id": room.roomid,
            "site_id": room.siteid,
            "capacity": room.capacity,
            "category": room.category,
            "classification": room.classification
        })
    return rooms


def _serialize_bookings(bookings):
    ret_bookings = []

    for bk in bookings:
        ret_bookings.append({
            "room": bk.roomname,
            "site_id": bk.roomid,
            "description": bk.descrip,
            "start_time": bk.starttime,
            "end_time": bk.finishtime,
            "contact": bk.contactname,
            "booking_id": bk.slotid
        })

    return ret_bookings
