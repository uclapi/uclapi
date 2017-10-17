from django.test import TestCase, SimpleTestCase

from .decorators import (
    how_many_seconds_until_midnight,
    get_var,
    throttle_api_call
)

from .helpers import generate_test_api_token

from freezegun import freeze_time
from rest_framework.test import APIRequestFactory


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
