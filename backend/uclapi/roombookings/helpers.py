from django.core.exceptions import FieldError, ObjectDoesNotExist
from .models import Booking, PageToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

import json
import datetime


def _create_page_token(query, pagination):
    page = PageToken(
        pagination=pagination,
        query=json.dumps(query, default=str)
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
    query = page.get_query()
    bookings, is_last_page = _paginated_result(
        query,
        page.curr_page,
        pagination
    )

    # if there is a next page
    bookings["next_page_exists"] = not is_last_page

    if not is_last_page:
        # append the page_token to return json
        bookings["page_token"] = page_token

    return bookings


def _paginated_result(query, page_number, pagination):
    try:
        all_bookings = Booking.objects.using('roombookings').filter(**query)
    except FieldError:
        return {
            "error": "something wrong with encoded query params"
        }, False

    paginator = Paginator(all_bookings, pagination)

    try:
        bookings = paginator.page(page_number)
    except PageNotAnInteger:
        # give first page
        bookings = paginator.page(1)
    except EmptyPage:
        # return empty page
        # bookings = paginator.page(paginator.num_pages)
        bookings = []

    serialized_bookings = _serialize_bookings(bookings)

    return (
        {"bookings": serialized_bookings},
        (page_number == paginator.num_pages)
    )


def _parse_datetime(start_time, end_time, search_date):
    try:
        if start_time:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()

        if end_time:
            end_time = datetime.datetime.strptime(end_time, '%H:%M').time()

        if not end_time and not start_time:
            if search_date:
                print(search_date)
                search_date = datetime.datetime.strptime(
                                            search_date, "%Y%m%d").date()
                day_start = datetime.time(0, 0, 1)  # start of the day
                day_end = datetime.time(23, 59, 59)  # end of the day
                start_time = datetime.datetime.combine(search_date, day_start)
                end_time = datetime.datetime.combine(search_date, day_end)
    except (TypeError, NameError, ValueError):
        return -1, -1, False

    return start_time, end_time, True


def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        rooms.append({
            "name": room.roomname,
            "roomid": room.roomid,
            "siteid": room.siteid,
            "sitename": room.sitename,
            "capacity": room.capacity,
            "classification": room.roomclass,
            "automated": room.automated,
            "location": {
                "address": [
                    room.address1,
                    room.address2,
                    room.address3,
                    room.address4
                ]
            }
        })
    return rooms


def _serialize_bookings(bookings):
    ret_bookings = []

    for bk in bookings:
        ret_bookings.append({
            "room": bk.roomname,
            "siteid": bk.siteid,
            "roomid": bk.roomid,
            "description": bk.descrip,
            "start_time": _kloppify(datetime.datetime.strftime(
                bk.startdatetime, "%Y-%m-%dT%H:%M:%S%z")),
            "end_time": _kloppify(datetime.datetime.strftime(
                bk.finishdatetime, "%Y-%m-%dT%H:%M:%S%z")),
            "contact": bk.condisplayname,
            "slotid": bk.slotid,
            "weeknumber": bk.weeknumber,
            "phone": bk.phone
        })

    return ret_bookings


def _serialize_equipment(equipment):
    ret_equipment = []

    for item in equipment:
        ret_equipment.append({
            "type": item.type,
            "description": item.description,
            "units": item.units
        })

    return ret_equipment


def _kloppify(date_string):
    return date_string[:-2] + ":" + date_string[-2:]


def _return_json_bookings(bookings):
    if "error" in bookings:
        return JsonResponse({
            "ok": False,
            "error": bookings["error"]
        })

    return JsonResponse({
        "ok": True,
        "bookings": bookings
    })
