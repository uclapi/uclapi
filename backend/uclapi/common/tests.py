from django.test import TestCase, SimpleTestCase

from .decorators import (
    _check_general_token_issues,
    _check_oauth_token_issues,
    _check_temp_token_issues,
    _get_last_modified_header,
    how_many_seconds_until_midnight,
    get_var,
    throttle_api_call,
    UclApiIncorrectTokenTypeException
)

from .helpers import (
    generate_api_token,
    PrettyJsonResponse as JsonResponse,
    RateLimitHttpResponse as HttpResponse
)

from dashboard.models import (
    App,
    User
)

from dashboard.app_helpers import get_temp_token, generate_temp_api_token

from oauth.models import OAuthToken, OAuthScope
from oauth.scoping import Scopes

from freezegun import freeze_time
from rest_framework.test import APIRequestFactory

from uclapi.settings import REDIS_UCLAPI_HOST

import datetime
import json
import redis
import time

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


class HttpResponseTestCase(TestCase):
    def test_check_headers_set(self):
        headers = {
            'Last-Modified': '1',
            'X-RateLimit-Limit': '2',
            'X-RateLimit-Remaining': '3',
            'X-RateLimit-Retry-After': '4'
        }
        response = HttpResponse(
            "hello",
            custom_header_data=headers
        )
        for key in headers:
            self.assertEqual(response[key], headers[key])


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
        token = generate_api_token("test")
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

    def test_throttle_bad_token_type(self):
        token = generate_api_token()
        with self.assertRaises(UclApiIncorrectTokenTypeException):
            (
                throttled,
                limit,
                remaining,
                reset_secs
            ) = throttle_api_call(token, "incorrect")


class TempTokenCheckerTest(TestCase):
    def setUp(self):
        self.valid_token = get_temp_token()

    def test_personal_data_requested(self):
        result = _check_temp_token_issues(
            self.valid_token,
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

    def test_token_does_not_exist(self):
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
            "Temporary token is either invalid or expired."
        )

    def test_invalid_path_requested(self):
        result = _check_temp_token_issues(
            self.valid_token,
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

    def test_page_token_provided(self):
        result = _check_temp_token_issues(
            self.valid_token,
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

    def test_expired_token_provided(self):
        r = redis.Redis(host=REDIS_UCLAPI_HOST)

        expired_token = generate_temp_api_token()
        # We initialise a new temporary token and set it to 1
        # as it is generated at its first usage.
        r.set(expired_token, 1, px=1)
        time.sleep(0.002)
        result = _check_temp_token_issues(
            expired_token,
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
            "Temporary token is either invalid or expired."
        )

    def test_all_passes(self):
        result = _check_temp_token_issues(
            self.valid_token,
            False,
            "/roombookings/bookings",
            None
        )
        self.assertEqual(
            result,
            self.valid_token
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

    def test_check_personal_data(self):
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

    def test_check_nonexistent_token(self):
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

    def test_check_all_ok(self):
        result = _check_general_token_issues(
            self.valid_app.api_token,
            False
        )
        self.assertEqual(
            result.api_token,
            self.valid_app.api_token
        )


class GenerateApiTokenTest(TestCase):
    def test_general_token_test(self):
        token = generate_api_token()
        self.assertEqual(
            len(token),
            70
        )
        self.assertEqual(
            token[:7],
            "uclapi-"
        )

    def test_temp_token_test(self):
        token = generate_api_token("temp")
        self.assertEqual(
            len(token),
            75
        )
        self.assertEqual(
            token[:12],
            "uclapi-temp-"
        )

    def test_user_token_test(self):
        token = generate_api_token("user")
        self.assertEqual(
            len(token),
            75
        )
        self.assertEqual(
            token[:12],
            "uclapi-user-"
        )


class OAuthTokenCheckerTest(TestCase):
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
        self.valid_user.save()

        self.valid_app = App.objects.create(
            user=self.valid_user,
            name="Test App"
        )
        self.valid_app.save()

        self.empty_scope = OAuthScope.objects.create(
            scope_number=0
        )
        self.empty_scope.save()

        s = Scopes()
        scope_num = s.add_scope(0, 'timetable')
        self.timetable_scope = OAuthScope.objects.create(
            scope_number=scope_num
        )
        self.timetable_scope.save()

        self.valid_oauth_token = OAuthToken.objects.create(
            app=self.valid_app,
            user=self.valid_user,
            scope=self.empty_scope
        )
        self.valid_oauth_token.save()

    def test_nonexistent_token(self):
        result = _check_oauth_token_issues(
            "uclapi-user-blah-blah-blah",
            "not-applicable",
            []
        )

        self.assertTrue(isinstance(result, JsonResponse))
        self.assertEqual(
            result.status_code,
            400
        )
        data = json.loads(result.content.decode())
        self.assertFalse(data["ok"])
        self.assertEqual(
            data["error"],
            "Token does not exist."
        )

    def test_bad_client_secret(self):
        result = _check_oauth_token_issues(
            self.valid_oauth_token.token,
            "incorrect-client-secret",
            []
        )
        self.assertTrue(isinstance(result, JsonResponse))
        self.assertEqual(
            result.status_code,
            400
        )
        data = json.loads(result.content.decode())
        self.assertFalse(data["ok"])
        self.assertEqual(
            data["error"],
            "Client secret incorrect."
        )

    def test_inactive_token(self):
        self.valid_oauth_token.active = False
        self.valid_oauth_token.save()

        result = _check_oauth_token_issues(
            self.valid_oauth_token.token,
            self.valid_app.client_secret,
            []
        )
        self.assertTrue(isinstance(result, JsonResponse))
        self.assertEqual(
            result.status_code,
            400
        )
        data = json.loads(result.content.decode())
        self.assertFalse(data["ok"])
        self.assertEqual(
            data["error"],
            "The token is inactive as the user has revoked "
            "your app's access to their data."
        )

    def test_wrong_scope(self):
        self.valid_oauth_token.active = True
        self.valid_oauth_token.save()

        result = _check_oauth_token_issues(
            self.valid_oauth_token.token,
            self.valid_app.client_secret,
            ['timetable']
        )
        self.assertTrue(isinstance(result, JsonResponse))
        self.assertEqual(
            result.status_code,
            400
        )
        data = json.loads(result.content.decode())
        self.assertFalse(data["ok"])
        self.assertEqual(
            data["error"],
            "The token provided does not have "
            "permission to access this data."
        )

    def test_valid_token(self):
        self.valid_oauth_token.scope = self.timetable_scope
        self.valid_oauth_token.save()

        result = _check_oauth_token_issues(
            self.valid_oauth_token.token,
            self.valid_app.client_secret,
            ['timetable']
        )

        self.assertEqual(
            result.token,
            self.valid_oauth_token.token
        )

    def test_deleted_app_valid_token(self):
        self.valid_oauth_token.active = True
        self.valid_oauth_token.save()
        self.valid_app.deleted = True
        self.valid_app.save()

        result = _check_oauth_token_issues(
            self.valid_oauth_token.token,
            self.valid_app.client_secret,
            ['timetable']
        )
        self.assertTrue(isinstance(result, JsonResponse))
        self.assertEqual(
            result.status_code,
            403
        )
        data = json.loads(result.content.decode())
        self.assertFalse(data["ok"])
        self.assertEqual(
            data["error"],
            "The token is invalid as the developer has "
            "deleted their app."
        )


class LastModifiedHeaderTestCase(TestCase):
    base_redis_key = "http:headers:Last-Modified:"

    def test_redis_case_1(self):
        redis_key = self.base_redis_key + __name__
        r = redis.Redis(host=REDIS_UCLAPI_HOST)
        r.set(
            redis_key,
            "2019-01-24T00:10:05+01:00"
        )
        last_modified_header = _get_last_modified_header(__name__)
        self.assertEqual(
            last_modified_header,
            "Wed, 23 Jan 2019 23:10:05 GMT"
        )
        r.delete(redis_key)

    def test_redis_case_2(self):
        redis_key = self.base_redis_key + __name__
        r = redis.Redis(host=REDIS_UCLAPI_HOST)
        r.set(
            redis_key,
            "2019-01-24T00:10:05+00:00"
        )
        last_modified_header = _get_last_modified_header(__name__)
        self.assertEqual(
            last_modified_header,
            "Thu, 24 Jan 2019 00:10:05 GMT"
        )
        r.delete(redis_key)

    def test_redis_case_3(self):
        redis_key = self.base_redis_key + __name__
        r = redis.Redis(host=REDIS_UCLAPI_HOST)
        r.set(
            redis_key,
            "2018-12-25T00:13:02-05:00"
        )
        last_modified_header = _get_last_modified_header(__name__)
        self.assertEqual(
            last_modified_header,
            "Tue, 25 Dec 2018 05:13:02 GMT"
        )
        r.delete(redis_key)

    def test_current_time_case_1(self):
        last_modified_header = _get_last_modified_header()
        current_time = datetime.datetime.utcnow()
        last_modified_timestamp = datetime.datetime.strptime(
            last_modified_header,
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        # We can't just assert that the timestamps will be exactly equal
        # as we can't guarantee that the testcase will all run within
        # one single second.

        # Thank you, Stack Overflow!
        # https://stackoverflow.com/a/4695663
        margin = datetime.timedelta(seconds=3)

        self.assertTrue(
            (
                last_modified_timestamp - margin
                <=
                current_time
                <=
                last_modified_timestamp + margin
            )
        )

    def test_redis_nonexistent_1(self):
        last_modified_header = _get_last_modified_header(
            "NONEXISTENTDONOTUSEABCXYZ"
        )
        current_time = datetime.datetime.utcnow()
        last_modified_timestamp = datetime.datetime.strptime(
            last_modified_header,
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        # We use the same assertions as the one for the current timestamp
        # as the key won't return any results.

        margin = datetime.timedelta(seconds=3)

        self.assertTrue(
            (
                last_modified_timestamp - margin
                <=
                current_time
                <=
                last_modified_timestamp + margin
            )
        )
