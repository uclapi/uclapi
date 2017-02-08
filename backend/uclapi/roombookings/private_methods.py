import datetime
from django.core.exceptions import FieldError
from .models import Booking, PageToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json


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

    page.curr_page += 1
    page.save()

    pagination = page.pagination
    query = json.loads(page.query)
    bookings = _paginated_result(query, page.curr_page, pagination)

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
        # return empty page
        # bookings = paginator.page(paginator.num_pages)
        bookings = {}

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
