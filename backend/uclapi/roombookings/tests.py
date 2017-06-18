import datetime
import json
import unittest.mock
from itertools import chain

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from freezegun import freeze_time
from rest_framework.test import APIRequestFactory

from dashboard.models import App, TemporaryToken, User

from .decorators import does_token_exist, log_api_call
from .helpers import (PrettyJsonResponse, _parse_datetime,
                      _serialize_equipment, how_many_seconds_until_midnight)
from .models import Lock, Room


class FakeModelClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class EquipmentSerializationTestCase(SimpleTestCase):

        def test_serialize_equipment(self):
            equipment_list = [
                FakeModelClass(
                    setid="LIVE-16-17",
                    roomid="016",
                    units=1,
                    description="Chairs with Tables",
                    siteid="267",
                    type="FF"
                ),
                FakeModelClass(
                    setid="LIVE-16-17",
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


class SecondsUntilMidnightTestCase(SimpleTestCase):
    def test_seconds_until_midnight(self):
        arg_list = [
            "2017-05-29 23:59:59",
            "2017-05-29 00:00:00",
            "2017-05-29 00:00:01"
        ]

        expected = [
            1,
            0,
            86399
        ]

        for idx, arg in enumerate(arg_list):
            with freeze_time(arg):
                self.assertEqual(
                    how_many_seconds_until_midnight(),
                    expected[idx]
                )


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
    def setUp(self):
        mock = unittest.mock.Mock()
        mock.status_code = 200
        self.dec_view = does_token_exist(
            unittest.mock.Mock(return_value=mock)
        )
        self.factory = APIRequestFactory()

        # this fixes a bug when the `test_temp_token_valid` test would fail
        TemporaryToken.objects.all().delete()

    def test_no_token_provided(self):
        request = self.factory.get('/a/random/path')
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No token provided")

    def test_invalid_token_provided(self):
        request = self.factory.get('/a/random/path', {'token': 'uclapi'})
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Token does not exist")

    def test_invalid_temp_token_provided(self):
        request = self.factory.get(
            '/a/random/path',
            {'token': 'uclapi-temp-invalid-token'}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Invalid temporary token")

    def test_temp_token_wrong_path(self):
        token = TemporaryToken.objects.create()

        request = self.factory.get('/a/path', {'token': token.api_token})
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token can only be used for /bookings"
        )

    def test_temp_token_page_token_provided(self):
        token = TemporaryToken.objects.create()

        request = self.factory.get(
            '/roombookings/bookings',
            {'token': token.api_token, 'page_token': 'next_page_comes_here'}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token can only return one booking"
        )

    def test_temp_token_overused(self):
        token = TemporaryToken.objects.create(uses=300)

        request = self.factory.get(
            '/roombookings/bookings', {'token': token.api_token}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token expired"
        )

    @unittest.mock.patch(
        'django.utils.timezone.now',
        lambda: datetime.datetime(2010, 10, 10, 10, 10, 10)
    )
    def test_temp_token_expired(self):
        token = TemporaryToken.objects.create()

        request = self.factory.get(
            '/roombookings/bookings', {'token': token.api_token}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Temporary token expired"
        )

    def test_temp_token_valid(self):
        token = TemporaryToken.objects.create()
        token.save()

        request = self.factory.get(
            '/roombookings/bookings', {'token': token.api_token}
        )
        response = self.dec_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(request.GET['results_per_page'], 1)
        self.assertEqual(
            TemporaryToken.objects.all()[0].uses,
            1
        )

    def test_normal_token_valid(self):
        user_ = User.objects.create(cn="test", employee_id=7357)
        app = App.objects.create(user=user_, name="An App")

        request = self.factory.get(
            '/roombookings/bookings', {'token': app.api_token}
        )
        response = self.dec_view(request)

        self.assertEqual(response.status_code, 200)


class LogApiCallTestCase(TestCase):
    def setUp(self):
        mock = unittest.mock.Mock()
        mock.status_code = 200
        self.dec_view = log_api_call(
            unittest.mock.Mock(return_value=mock)
        )
        self.factory = APIRequestFactory()

        # make tests work
        App.objects.all().delete()
        User.objects.all().delete()

    @unittest.mock.patch('keen.add_event')
    def test_log_api_call_temp_token(self, keen_instance):
        request = self.factory.get(
            '/roombookings/bookings', {'token': 'uclapi-temp-not-real'}
        )
        response = self.dec_view(request)

        event, args = keen_instance.call_args[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event, "apicall")
        self.assertEqual(args['method'], "bookings")
        self.assertEqual(args['service'], "roombookings")
        self.assertTrue(args['temp_token'])
        self.assertEqual(
            args['queryparams']['token'][0],
            'uclapi-temp-not-real'
        )

    @unittest.mock.patch('keen.add_event')
    def test_log_api_call_normal_token(self, keen_instance):
        user_ = User.objects.create(
            email="test@ucl.ac.uk", cn="test",
            given_name="Test Test"
        )
        app = App.objects.create(user=user_, name="An App")

        request = self.factory.get(
            '/roombookings/bookings',
            # GET args
            {'token': app.api_token},
            # headers
            **{'HTTP_UCLAPI_ROOMBOOKINGS_VERSION': 1}
        )
        response = self.dec_view(request)

        event, args = keen_instance.call_args[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event, "apicall")
        self.assertEqual(args['name'], "Test Test")
        self.assertEqual(args['email'], "test@ucl.ac.uk")
        self.assertEqual(args['method'], "bookings")
        self.assertEqual(args['service'], "roombookings")
        self.assertEqual(
            args['version-headers']['HTTP_UCLAPI_ROOMBOOKINGS_VERSION'],
            1
        )
        self.assertEqual(
            args['queryparams']['token'][0],
            app.api_token
        )
