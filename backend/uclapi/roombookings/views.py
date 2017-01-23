from functools import reduce

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

    # functional filters
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    """
    filter by non-time params first
    then start_time_gte and end_time_lte
    """
    bookings = Booking.objects.filter(**request_params)

    if start_time:
        booking.filter(start_time_gte=start_time)

    if end_time:
        booking.filter(end_time_lte=end_time)

    return Response(_serialize_bookings(booking))


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
            "contact": bk.contact
        })

    return Response(ret_bookings)
