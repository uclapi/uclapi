from functools import reduce

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime

# Create your views here.
from .models import Booking, Room


@api_view(['GET'])
def get_rooms(request):
    # add them to iterables so can be filtered without if-else
    request_params = {}

    request_params['room_id'] = request.GET.get('room_id')
    request_params['site_id'] = request.GET.get('site_id')
    request_params['name'] = request.GET.get('name')
    request_params['category'] = request.GET.get('category')
    request_params['room_type'] = request.GET.get('type')
    request_params['classification'] = request.GET.get('classification')
    request_params['campus_id'] = request.GET.get('campus_id')
    request_params['capacity'] = request.GET.get('capacity')

    # webview available rooms
    all_rooms = Room.objects.filter(
            setid='LIVE16-17',
            centrally_bookable=True,
            webview=True
        )

    # no filters provided, return all rooms serialised
    if not reduce(lambda x, y: x or y, request_params.values()):
        return Response(_serialize_rooms(all_rooms))

    filtered_rooms = all_rooms.filter(**request_params)

    return Response(_serialize_rooms(filtered_rooms))


@api_view(['GET'])
def get_booking(request):
    # query params
    request_params = {}

    # non functional filters
    request_params['room_id'] = request.GET.get('room_id')
    # TODO: building?
    request_params['site_id'] = request.GET.get('site_id')
    request_params['description'] = request.GET.get('description')
    request_params['contact'] = request.GET.get('contact')
    request_params['date'] = request.GET.get('date')

    # functional filters
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    if any([start_time, end_time, request_params['date']]):
        start_time, end_time, request_params['date'], is_parsed =
        _parse_datetime(
            start_time,
            end_time,
            request_params['date']
        )

    if not is_parsed:
        return Response({
            "error": "date/time isn't formatted as suggested in the docs"
        })

    """
    filter by non-time params first
    then start_time_gte and end_time_lte
    """
    bookings = Booking.objects.filter(**request_params)

    if start_time:
        bookings.filter(start_time_gte=start_time)

    if end_time:
        bookings.filter(end_time_lte=end_time)

    return Response(_serialize_bookings(bookings))


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
            "name": room.NAME,
            "room_id": room.ROOMID,
            "site_id": room.SITEID,
            "type": room.TYPE,
            "capacity": room.CAPACITY,
            "campus_id": room.CAMPUSID
        })
    return rooms


def _serialize_bookings(bookings):
    ret_bookings = []

    for bk in bookings:
        ret_bookings.append({
            "room": bk.room.NAME,
            "site_id": bk.room.site_id,
            "description": bk.description,
            "start_time": bk.start_time,
            "end_time": bk.end_time,
            "contact": bk.contact,
            "booking_id": bk.id
        })

    return ret_bookings
