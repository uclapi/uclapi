from django.test import TestCase, SimpleTestCase

from .decorators import (
    _check_general_token_issues,
    _check_temp_token_issues,
    how_many_seconds_until_midnight,
    get_var,
    throttle_api_call
)

from .helpers import (
    generate_test_api_token,
    PrettyJsonResponse as JsonResponse
)

from dashboard.models import (
    App,
    TemporaryToken,
    User
)

from freezegun import freeze_time
from rest_framework.test import APIRequestFactory

import datetime
import json


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


class GetVarTestCase(TestCase):
    test_factory = APIRequestFactory()

    def test_get_parameters(self):
        request = self.test_factory.get(
            '/test/test?parameter1=five&parameter2=20'
        )
        p1 = get_var(request, "parameter1")
        p2 = get_var(request, "parameter2")

        self.assertEqual(p1, "five")
        self.assertEqual(p2, "20")

    def test_post_parameters(self):
        request = self.test_factory.post('/test/test', {
            "username": "testuser",
            "password": "apassword!$",
            "some_number": 123
        })

        p1 = get_var(request, "username")
        p2 = get_var(request, "password")
        p3 = get_var(request, "some_number")

        self.assertEqual(p1, "testuser")
        self.assertEqual(p2, "apassword!$")
        self.assertEqual(p3, "123")

    def test_get_and_post_parameters(self):
        request = self.test_factory.post(
            '/test/test?get_param_1=test_param',
            {
                "post_param_1": "testcase",
                "post_param_2": "some_other_param_case",
                "something_else": "$$$!!!___***"
            }
        )

        p1 = get_var(request, "get_param_1")
        p2 = get_var(request, "post_param_1")
        p3 = get_var(request, "post_param_2")
        p4 = get_var(request, "something_else")

        self.assertEqual(p1, "test_param")
        self.assertEqual(p2, "testcase")
        self.assertEqual(p3, "some_other_param_case")
        self.assertEqual(p4, "$$$!!!___***")


class ThrottleApiCallTest(TestCase):
    def test_throttling(self):
        token = generate_test_api_token()
        (
            throttled,
            limit,
            remaining,
            reset_secs
        ) = throttle_api_call(token, "test-token")

        self.assertFalse(throttled)
        self.assertEqual(limit, 1)
        self.assertEqual(remaining, 0)
        # Not testing reset_secs as this is handled by testing
        # the how_many_seconds_until_midnight() function above

        (
            throttled,
            limit,
            remaining,
            reset_secs
        ) = throttle_api_call(token, "test-token")

        self.assertTrue(throttled)
        self.assertEqual(limit, 1)
        self.assertEqual(remaining, 0)


class TempTokenCheckerTest(TestCase):
    def setUp(self):
        self.valid_token = TemporaryToken.objects.create()

    def personal_data_requested(self):
        result = _check_temp_token_issues(
            self.valid_token.token_code,
            True,
            "/roombookings/bookings",
            None
        )
        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Personal data requires OAuth."
        )

    def token_does_not_exist(self):
        invalid_token = "uclapi-temp-this-token-does-not-exist"
        result = _check_temp_token_issues(
            invalid_token,
            False,
            "/roombookings/bookings",
            None
        )
        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Invalid temporary token."
        )

    def invalid_path_requested(self):
        result = _check_temp_token_issues(
            self.valid_token.token_code,
            False,
            "/roombookings/some_other_path",
            None
        )
        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Temporary token can only be used for /bookings."
        )

    def page_token_provided(self):
        result = _check_temp_token_issues(
            self.valid_token.token_code,
            False,
            "/roombookings/bookings",
            "abcdefgXYZ"
        )
        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Temporary token can only return one booking."
        )

    def expired_token_provided(self):
        expired_token = TemporaryToken.objects.create(
            created=datetime.datetime(2010, 1, 1, 1, 0)
        )
        result = _check_temp_token_issues(
            expired_token.token_code,
            False,
            "/roombookings/bookings",
            None
        )
        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Temporary token expired."
        )

    def all_passes(self):
        result = _check_temp_token_issues(
            self.valid_token.token_code,
            False,
            "/roombookings/bookings",
            None
        )
        self.assertEqual(
            result.token_code,
            self.valid_token.token_code
        )


class GeneralTokenCheckerTest(TestCase):
    def setUp(self):
        self.valid_user = User.objects.create(
            email="testuserabc@ucl.ac.uk",
            full_name="Test User",
            given_name="Test",
            cn="test2",
            department="Dept. of Tests",
            employee_id="TESTU12345",
            raw_intranet_groups="test1;test2",
            agreement=True
        )
        self.valid_app = App.objects.create(
            user=self.valid_user,
            name="Test App"
        )

    def check_personal_data(self):
        result = _check_general_token_issues(
            self.valid_app.api_token,
            True
        )

        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Personal data requires OAuth."
        )

    def check_nonexistent_token(self):
        result = _check_general_token_issues(
            "uclapi-blah-blah-blah",
            False
        )

        self.assertTrue(isinstance(result, JsonResponse))
        data = json.loads(result.content.decode())
        self.assertEqual(result.status_code, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(
            data['error'],
            "Token does not exist."
        )

    def check_all_ok(self):
        result = _check_general_token_issues(
            self.valid_app.api_token,
            False
        )
        self.assertEqual(
            result.api_token,
            self.valid_app.api_token
        )
