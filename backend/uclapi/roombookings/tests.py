import datetime
import json
import unittest.mock
from itertools import chain, repeat

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIRequestFactory
from django.conf import settings
from django_mock_queries.query import MockSet, MockModel

from dashboard.models import App, TemporaryToken, User

from .helpers import (_filter_for_free_rooms, _localize_time,
                      PrettyJsonResponse, _parse_datetime,
                      _round_date, _serialize_equipment)
from .models import Lock, Room

from .views import get_bookings


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
            (datetime.datetime(2016, 2, 19, 0, 0, 1),
                datetime.datetime(2016, 2, 19, 23, 59, 59), True),
            (datetime.datetime(2017, 3, 20, 0, 0, 1),
                datetime.datetime(2017, 3, 20, 23, 59, 59), True),
            (datetime.datetime(2017, 12, 14, 0, 0, 1),
                datetime.datetime(2017, 12, 14, 23, 59, 59), True),
            (datetime.datetime(2017, 10, 8, 0, 0, 1),
                datetime.datetime(2017, 10, 8, 23, 59, 59), True),
            (datetime.datetime(2017, 1, 1, 0, 0, 1),
                datetime.datetime(2017, 1, 1, 23, 59, 59), True),
            (datetime.datetime(2018, 1, 1, 0, 0, 1),
                datetime.datetime(2018, 1, 1, 23, 59, 59), True),
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
            bookingA=True,
            bookingB=False
        )
    )

    lock_objects = unittest.mock.patch(
        'roombookings.models.Lock.objects',
        fake_locks
    )

    def setUp(self):
        self.factory = APIRequestFactory()

        # This fixes a bug when the `test_temp_token_valid` test would fail
        TemporaryToken.objects.all().delete()

        # General temporary token for tests
        self.token = TemporaryToken.objects.create()
        self.token.save()

        # An expired token for the expiry test
        self.expired_token = TemporaryToken.objects.create()
        self.expired_token.save()
        self.expired_token.created = datetime.datetime(
            2010, 10, 10, 10, 10, 10
        )
        self.expired_token.save()

        # A valid token to use later
        self.valid_token = TemporaryToken.objects.create()
        self.valid_token.save()

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
        self.assertEqual(content["error"], "Invalid temporary token.")

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_wrong_path(self):
        request = self.factory.get('/a/path', {'token': self.token.api_token})
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
                'token': self.token.api_token,
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
            '/roombookings/bookings', {'token': self.token.api_token}
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
    def test_temp_token_expired(self):
        request = self.factory.get(
            '/roombookings/bookings', {
                'token': self.expired_token.api_token
            }
        )
        response = get_bookings(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token expired."
        )

    @booking_objects
    @bookinga_objects
    @bookingb_objects
    @lock_objects
    def test_temp_token_valid(self):
        request = self.factory.get(
            '/roombookings/bookings', {'token': self.valid_token.api_token}
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
