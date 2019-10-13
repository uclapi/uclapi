import datetime
import json
import unittest.mock
from itertools import chain, repeat

import redis

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIRequestFactory
from django.conf import settings
from django_mock_queries.query import MockSet, MockModel

from dashboard.app_helpers import get_temp_token
from dashboard.models import App, User

from .helpers import (
    _create_page_token,
    _filter_for_free_rooms,
    _localize_time,
    _parse_datetime,
    _round_date,
    _serialize_equipment,
    PrettyJsonResponse,
    TOKEN_EXPIRY_TIME
)

from .models import Room
from timetable.models import Lock

from .views import get_bookings

from uclapi.settings import REDIS_UCLAPI_HOST


class FakeModelClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class EquipmentSerializationTestCase(SimpleTestCase):

        def test_serialize_equipment(self):
            equipment_list = [
                FakeModelClass(
                    setid=settings.ROOMBOOKINGS_SETID,
                    roomid="016",
                    units=1,
                    description="Chairs with Tables",
                    siteid="267",
                    type="FF"
                ),
                FakeModelClass(
                    setid=settings.ROOMBOOKINGS_SETID,
                    roomid="105",
                    units=1,
                    description="Software - Earth Sciences - self learning",
                    siteid="002",
                    type="FF"
                )
            ]
            none_qs = Room.objects.none()
            equipment_qs = list(chain(none_qs, equipment_list))
            serialised_equipment = _serialize_equipment(equipment_qs)
            self.assertEqual(
                serialised_equipment, [
                    {
                        "type": "FF",
                        "description": "Chairs with Tables",
                        "units": 1
                    },
                    {
                        "type": "FF",
                        "description": (
                            "Software - Earth Sciences"
                            " - self learning"
                        ),
                        "units": 1
                    }
                ]
            )


class ParseDateTimeTestCase(SimpleTestCase):
    def test_parse_datetime(self):
        arg_list = [
            # valid dates
            [None, None, "20160219"],
            [None, None, "20170320"],
            [None, None, "20171214"],
            [None, None, "20171008"],
            [None, None, "20170101"],
            [None, None, "20180101"],
            # invalid dates
            [None, None, "31001312"],
            [None, None, "20170229"],
            [None, None, "20172323"],
            [None, None, "20198989"],
            # only start time
            ["2017-05-16T11:34:39+00:00", None, "342453"],
            ["2017-01-16T23:34:39+00:00", None, "334533"],
            ["2017-02-16T11:34:39+00:00", None, "334533"],
            # only end time
            [None, "2017-01-16T23:34:39+00:00", "334533"],
            # invalid start and end
            ["2012-16T11:34:39+00:00", None, "334533"],
            [None, "23424", "324254"],
            # both end and start time
            ["2017-05-16T11:34:39+00:00", "2018-05-16T11:34:39+00:00", "3423"],
            ["2017-12-16T10:00:00+00:00", "2018-06-16T10:00:00+00:00", "3"],
        ]

        expected = [
            (datetime.datetime(2016, 2, 19, 0, 0, 0, 0),
                datetime.datetime(2016, 2, 19, 23, 59, 59, 999999), True),
            (datetime.datetime(2017, 3, 20, 0, 0, 0, 0),
                datetime.datetime(2017, 3, 20, 23, 59, 59, 999999), True),
            (datetime.datetime(2017, 12, 14, 0, 0, 0, 0),
                datetime.datetime(2017, 12, 14, 23, 59, 59, 999999), True),
            (datetime.datetime(2017, 10, 8, 0, 0, 0, 0),
                datetime.datetime(2017, 10, 8, 23, 59, 59, 999999), True),
            (datetime.datetime(2017, 1, 1, 0, 0, 0, 0),
                datetime.datetime(2017, 1, 1, 23, 59, 59, 999999), True),
            (datetime.datetime(2018, 1, 1, 0, 0, 0, 0),
                datetime.datetime(2018, 1, 1, 23, 59, 59, 999999), True),
            (-1, -1, False),
            (-1, -1, False),
            (-1, -1, False),
            (-1, -1, False),
            (datetime.datetime(2017, 5, 16, 12, 34, 39), None, True),
            (datetime.datetime(2017, 1, 16, 23, 34, 39), None, True),
            (datetime.datetime(2017, 2, 16, 11, 34, 39), None, True),
            (None, datetime.datetime(2017, 1, 16, 23, 34, 39), True),
            (-1, -1, False),
            (-1, -1, False),
            (datetime.datetime(2017, 5, 16, 12, 34, 39),
                datetime.datetime(2018, 5, 16, 12, 34, 39), True),
            (datetime.datetime(2017, 12, 16, 10, 0, 0),
                datetime.datetime(2018, 6, 16, 11, 0, 0), True)
        ]

        for index, args in enumerate(arg_list):
            self.assertEqual(
                expected[index],
                _parse_datetime(args[0], args[1], args[2])
            )


class PrettyPrintJsonTestCase(SimpleTestCase):
    def test_pretty_print(self):
        response = PrettyJsonResponse({"foo": "bar"})
        self.assertEqual(response.content.decode(), '{\n    "foo": "bar"\n}')


class ManagementCommandsTestCase(TestCase):
    def test_create_lock(self):
        L = len(Lock.objects.all())

        self.assertGreaterEqual(L, 0)
        self.assertLessEqual(L, 1)

        call_command('create_lock')

        self.assertEqual(
            len(Lock.objects.all()),
            1
        )


class DoesTokenExistTestCase(TestCase):
    # Sets up some fake bookings
    fake_bookings = MockSet(
        MockModel(
            setid='LIVE-17-18',
            finishtime='16:00',
            id=8869,
            weeknumber=12.0,
            starttime='13:00',
            bookabletype='CB',
            title='Some topic',
            finishdatetime=datetime.datetime(2017, 11, 14, 16, 0),
            descrip='8 x rooms needed',
            slotid=1662773,
            sitename='IOE - Bedford Way, 20',
            phone=None,
            siteid='162',
            roomname='IOE - Bedford Way (20) - 790',
            condisplayname='Some Lecturer',
            startdatetime=datetime.datetime(2017, 11, 14, 13, 0),
            roomid='790',
            bookingid=None
        ),
        MockModel(
            setid='LIVE-17-18',
            finishtime='12:30',
            id=13692,
            weeknumber=21.0,
            starttime='11:00',
            bookabletype='CB',
            title='Another topic',
            finishdatetime=datetime.datetime(2018, 1, 19, 12, 30),
            descrip=None,
            slotid=1673854,
            sitename='IOE - Bedford Way, 20',
            phone=None,
            siteid='162',
            roomname='Some other room',
            condisplayname='Some other lecturer',
            startdatetime=datetime.datetime(2018, 1, 19, 11, 0),
            roomid='418',
            bookingid=None
        )
    )
    booking_objects = unittest.mock.patch(
        'roombookings.models.Booking.objects',
        fake_bookings
    )
    bookinga_objects = unittest.mock.patch(
        'roombookings.models.BookingA.objects',
        fake_bookings
    )
    bookingb_objects = unittest.mock.patch(
        'roombookings.models.BookingB.objects',
        fake_bookings
    )

    fake_locks = MockSet(
        MockModel(
            a=True,
            b=False
        )
    )

    lock_objects = unittest.mock.patch(
        'timetable.models.Lock.objects',
        fake_locks
    )

    def setUp(self):
        self.factory = APIRequestFactory()

        # General temporary token for tests
        self.token = get_temp_token()

        # A valid token to use later
        self.valid_token = get_temp_token()

        # Standard Token data
        self.user_ = User.objects.create(cn="test", employee_id=7357)
        self.app = App.objects.create(user=self.user_, name="An App")

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_no_token_provided(self):
        request = self.factory.get('/a/random/path')
        response = get_bookings(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No token provided.")

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_invalid_token_provided(self):
        request = self.factory.get('/a/random/path', {'token': 'uclapi'})
        response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Token is invalid.")

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_invalid_temp_token_provided(self):
        request = self.factory.get(
            '/a/random/path',
            {'token': 'uclapi-temp-invalid-token'}
        )
        response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token is either invalid or expired."
        )

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_wrong_path(self):
        request = self.factory.get('/a/path', {'token': self.token})
        response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token can only be used for /bookings."
        )

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_page_token_provided(self):
        request = self.factory.get(
            '/roombookings/bookings',
            {
                'token': self.token,
                'page_token': 'next_page_comes_here'
            }
        )
        response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token can only return one booking."
        )

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_overused(self):
        request = self.factory.get(
            '/roombookings/bookings', {'token': self.token}
        )
        for _ in repeat(None, 11):
            response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 429)
        self.assertFalse(content["ok"])
        self.assertEqual(
            "You have been throttled. Please try again in ",
            content["error"][:45]
        )

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_valid(self):
        request = self.factory.get(
            '/roombookings/bookings', {'token': self.valid_token}
        )
        response = get_bookings(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.GET['results_per_page'], 1)

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_normal_token_valid(self):
        request = self.factory.get(
            '/roombookings/bookings', {'token': self.app.api_token}
        )
        response = get_bookings(request)

        self.assertEqual(response.status_code, 200)


class RoundDateTestCase(SimpleTestCase):
    def test_round_down(self):
        time_string = "2017-10-25T03:36:45+00:00"
        round_down = _round_date(_localize_time(time_string))
        date = datetime.date(2017, 10, 25)
        self.assertEqual(round_down, date)

    def test_round_up(self):
        time_string = "2017-10-25T03:36:45+00:00"
        round_down = _round_date(_localize_time(time_string), up=True)
        date = datetime.date(2017, 10, 26)
        self.assertEqual(round_down, date)


class FilterFreeRoomsTestCase(SimpleTestCase):
    def test_empty_rooms_and_bookings(self):
        start = datetime.date(2017, 10, 25)
        end = datetime.date(2017, 10, 26)
        result = _filter_for_free_rooms([], [], start, end)
        self.assertEqual(result, [])

    def test_empty_bookings(self):
        start = datetime.date(2017, 10, 25)
        end = datetime.date(2017, 10, 26)
        rooms = [
            {"roomid": 1, "siteid": 1},
        ]
        result = _filter_for_free_rooms(rooms, [], start, end)
        self.assertEqual(result, rooms)


class CreateRedisPageTokenTest(TestCase):
    def test_create_page_token(self):
        query = {"test": "test_data"}
        pagination = 'pagination_data'
        page_token = _create_page_token(
            query,
            pagination
        )

        r = redis.Redis(host=REDIS_UCLAPI_HOST)

        ttl = r.ttl(page_token)

        # Python Redis 3.0+ now always returns an int
        # If it returns:
        # -1: The key has no TTL set
        # -2: The key does not exist
        self.assertTrue(ttl > 0)
        self.assertTrue(ttl <= TOKEN_EXPIRY_TIME)

        data = json.loads(r.get(page_token).decode('ascii'))
        self.assertEqual(
            data["current_page"],
            0
        )
        self.assertEqual(
            data["pagination"],
            pagination
        )
        query_decoded = json.loads(data["query"])
        self.assertEqual(
            query_decoded["test"],
            "test_data"
        )


class GetBookingEndpointTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        # Standard Token data
        self.user_ = User.objects.create(cn="test", employee_id=7357)
        self.app = App.objects.create(user=self.user_, name="An App")

    # TODO: Github issue #1155
    # def test_get_booking_default(self):
    #     request = self.factory.get(
    #         '/roombookings/bookings',
    #         {'token': self.app.api_token}
    #     )
    #     response = get_bookings(request)
    #     self.assertEqual(response.status_code, 200)

    def test_get_booking_invalid_results_per_page(self):
        request = self.factory.get(
            '/roombookings/bookings',
            {'token': self.app.api_token, 'results_per_page': 'ten'}
        )
        response = get_bookings(request)
        self.assertEqual(response.status_code, 400)
