from __future__ import unicode_literals

from django.core.exceptions import FieldError, ObjectDoesNotExist
from .models import PageToken, BookingA, BookingB, Lock, Location
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import django.http

import json
import datetime
import pytz
from datetime import timedelta
import ciso8601

class PrettyJsonResponse(django.http.JsonResponse):
    def __init__(self, data):
        super().__init__(data, json_dumps_params={'indent': 4})
        
JsonResponse = PrettyJsonResponse

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
        lock = Lock.objects.all()[0]
        curr = BookingA if not lock.bookingA else BookingB
        all_bookings = curr.objects.filter(**query)
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


def _localize_time(time_string):
    london_time = pytz.timezone("Europe/London")
    ret_time = time_string.replace(" ", "+")
    ret_time = ciso8601.parse_datetime(ret_time)
    ret_time = ret_time.astimezone(london_time)
    return ret_time.replace(tzinfo=None)



def _parse_datetime(start_time, end_time, search_date):
    parsed_start_time, parsed_end_time = None, None
    try:
        if start_time:
            # + gets decoded into a space in params
            parsed_start_time = _localize_time(start_time)

        if end_time:
            parsed_end_time = _localize_time(end_time)

        if not end_time and not start_time:
            if search_date:
                search_date = datetime.datetime.strptime(
                                            search_date, "%Y%m%d").date()
                day_start = datetime.time(0, 0, 1)  # start of the day
                day_end = datetime.time(23, 59, 59)  # end of the day
                parsed_start_time = datetime.datetime.combine(
                    search_date,
                    day_start
                )
                parsed_end_time = datetime.datetime.combine(
                    search_date,
                    day_end
                )
    except (TypeError, NameError, ValueError, AttributeError):
        return -1, -1, False

    return parsed_start_time, parsed_end_time, True


def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        room_to_add = {
            "roomname": room.roomname,
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
        }
        try:
            location = Location.objects.get(
                siteid=room.siteid,
                roomid=room.roomid
            )
            room_to_add['location']['coordinates'] = {
                "lat": location.lat,
                "lng": location.lng
            }
        except ObjectDoesNotExist:
            # no location for this room, leave out
            pass

        rooms.append(room_to_add)
    return rooms


def _serialize_bookings(bookings):
    ret_bookings = []
    for bk in bookings:
        ret_bookings.append({
            "roomname": bk.roomname,
            "siteid": bk.siteid,
            "roomid": bk.roomid,
            "description": bk.descrip,
            "start_time": _kloppify(datetime.datetime.strftime(
                bk.startdatetime, "%Y-%m-%dT%H:%M:%S"), bk.startdatetime),
            "end_time": _kloppify(datetime.datetime.strftime(
                bk.finishdatetime, "%Y-%m-%dT%H:%M:%S"), bk.finishdatetime),
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


def _kloppify(date_string, date):
    local_time = pytz.timezone('Europe/London')

    if (local_time.localize(date).dst() > timedelta(0)):
        return date_string + "+01:00"
    else:
        return date_string + "+00:00"


def _return_json_bookings(bookings):
    if "error" in bookings:
        return JsonResponse({
            "ok": False,
            "error": bookings["error"]
        })

    bookings["ok"] = True

    return JsonResponse(bookings)

def how_many_seconds_until_midnight():
    """Returns the number of seconds until midnight."""
    tomorrow = datetime.datetime.now() + timedelta(days=1)
    midnight = datetime.datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
    return (midnight - datetime.datetime.now()).seconds
