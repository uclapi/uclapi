from __future__ import unicode_literals

import datetime
import json
from datetime import timedelta

import ciso8601
import pytz
import redis

from django.conf import settings
from django.core.exceptions import FieldError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from .api_helpers import generate_token
from .models import BookingA, BookingB, Location, SiteLocation
from common.helpers import PrettyJsonResponse
from timetable.models import Lock


TOKEN_EXPIRY_TIME = 30 * 60

ROOM_TYPE_MAP = {
    "AN": "Anechoic Chamber",
    "CI": "Clinic Room",
    "CF": "Catering Facilities",
    "CFE": "Cafe",
    "CL": "Cloakroom",
    "CR": "Classroom",
    "ER": "Equipment Room",
    "IN": "Installation",
    "LA": "Laboratory",
    "LB": "Library",
    "LT": "Lecture Theatre",
    "MR": "Meeting Room",
    "OF": "Office",
    "PC1": "Public Cluster",
    "PC2": "Public Cluster - Tutorial",
    "PC3": "Public Cluster - Students",
    "RC": "Reverberation Chamber",
    "SS": "Social Space",
    "STU": "Studio",
    "TH": "Theatre",
}


def _create_page_token(query, pagination):
    r = redis.Redis(host=settings.REDIS_UCLAPI_HOST)
    page_data = {
        "current_page": 0,
        "pagination": pagination,
        "query": json.dumps(query, default=str),
    }
    page_token = generate_token()
    r.set(page_token, json.dumps(page_data), ex=TOKEN_EXPIRY_TIME)
    return page_token


def _get_paginated_bookings(page_token):
    r = redis.Redis(host=settings.REDIS_UCLAPI_HOST)
    try:
        page_data = json.loads(r.get(page_token).decode('ascii'))
    except (AttributeError, json.decoder.JSONDecodeError):
        return {
            "error": "Page token does not exist"
        }

    page_data["current_page"] += 1
    r.set(page_token, json.dumps(page_data), ex=TOKEN_EXPIRY_TIME)

    pagination = page_data["pagination"]
    query = json.loads(page_data["query"])
    bookings, is_last_page = _paginated_result(
        query,
        page_data["current_page"],
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
        curr = BookingA if lock.a else BookingB
        all_bookings = curr.objects.filter(
            Q(bookabletype='CB') | Q(siteid='238') | Q(siteid='240'),
            **query
        ).order_by('startdatetime')
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


def _round_date(time_string, up=False):
    """
    Rounds the datetime to the nearest day.
    Rounds down by default until up is passed as True in which case
    it rounds up
    """
    date = datetime.date(
        time_string.year,
        time_string.month,
        time_string.day
    )

    if up:
        date += datetime.timedelta(days=1)

    return date


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
                parsed_start_time = datetime.datetime.combine(
                    search_date,
                    datetime.time.min  # start of the day
                )
                parsed_end_time = datetime.datetime.combine(
                    search_date,
                    datetime.time.max  # end of the day
                )
    except (TypeError, NameError, ValueError, AttributeError):
        return -1, -1, False

    return parsed_start_time, parsed_end_time, True


def _serialize_rooms(room_set):
    rooms = []
    for room in room_set:
        # Maps room classification to a textual version
        # e.g. LT => Lecture Theatre
        classification_name = ROOM_TYPE_MAP.get(
            room.roomclass,
            "Unknown Room Type"
        )
        room_to_add = {
            "roomname": room.roomname,
            "roomid": room.roomid,
            "siteid": room.siteid,
            "sitename": room.sitename,
            "capacity": room.capacity,
            "classification": room.roomclass,
            "classification_name": classification_name,
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
        except Location.DoesNotExist:
            # no location for this room, try building
            try:
                location = SiteLocation.objects.get(
                    siteid=room.siteid
                )
                room_to_add['location']['coordinates'] = {
                    "lat": location.lat,
                    "lng": location.lng
                }
            except SiteLocation.DoesNotExist:
                # no location for this room
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
            "description": bk.title,
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
    return date_string + "+00:00"


def _return_json_bookings(bookings, custom_header_data=None):
    if "error" in bookings:
        return PrettyJsonResponse({
            "ok": False,
            "error": bookings["error"]
        }, custom_header_data)

    bookings["ok"] = True

    return PrettyJsonResponse(bookings, custom_header_data)


def how_many_seconds_until_midnight():
    """Returns the number of seconds until midnight."""
    tomorrow = datetime.datetime.now() + timedelta(days=1)
    midnight = datetime.datetime(
        year=tomorrow.year, month=tomorrow.month,
        day=tomorrow.day, hour=0, minute=0, second=0
    )
    return (midnight - datetime.datetime.now()).seconds


def _create_map_of_overlapping_bookings(bookings, start, end):
    """
    Creates map of room to bookings where each booking overlaps
    with the given time range
    """
    bookings_map = {}

    for booking in bookings:
        booking_start = _localize_time(booking["start_time"])
        booking_end = _localize_time(booking["end_time"])

        if _overlaps(
            start1=booking_start,
            end1=booking_end,
            start2=start,
            end2=end
        ):
            roomid, siteid = booking["roomid"], booking["siteid"]
            bookings_map[(roomid, siteid)] = bookings_map.get(
                (roomid, siteid), []
            ) + [booking]

    return bookings_map


def _overlaps(start1, end1, start2, end2):
    """
    takes 4 datetimes
    checks if they overlap
    """
    return max(start1, start2) < min(end1, end2)


def _filter_for_free_rooms(all_rooms, bookings, start, end):
    """
    Find all rooms which don't have any bookings.
    Args:
        all_rooms: All available rooms.
        bookings: All the bookings made in the days of the given time period
        start: Start time for free rooms
        end: End time for free rooms
    """
    rooms_with_bookings = list(all_rooms)
    bookings_map = _create_map_of_overlapping_bookings(bookings, start, end)

    free_rooms = []
    for room in rooms_with_bookings:
        roomid, siteid = room["roomid"], room["siteid"]
        if (
            (roomid, siteid) not in bookings_map or
            not bookings_map[(roomid, siteid)]
        ):
            # if room doesn't have any overlapping bookings
            free_rooms.append(room)

    return free_rooms
