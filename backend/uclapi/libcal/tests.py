import os
from unittest import mock
from urllib import parse

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from parameterized import parameterized
from rest_framework.test import APIClient
import requests_mock
import redis

from dashboard.models import App, User
from uclapi.settings import REDIS_UCLAPI_HOST


def all_params(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name('_'.join(str(x) for x in param.args)),
    )


def all_params_except_libcal_endpoint(testcase_func, param_num, param):
    return "%s_%s" % (
        testcase_func.__name__,
        parameterized.to_safe_name('_'.join(str(param.args[x]) for x in range(len(param.args)) if x != 1)),
    )


@requests_mock.Mocker()
@mock.patch.dict(
    os.environ,
    {
        "LIBCAL_BASE_URL": "https://library-calendars.ucl.ac.uk",
        "LIBCAL_CLIENT_ID": '123',
        "LIBCAL_CLIENT_SECRET": "secret"
    }
)
class LibCalManagementCommandTestCase(SimpleTestCase):
    """Tests for the LibCal refresh_libcal_token management command."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.r: redis.Redis = redis.Redis(
            host=REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )

    def test_command_sets_token_in_redis(self, m):
        """Tests that a successful call to the endpoint correctly saved the token in Redis."""
        token: str = "random-str"
        response = {'expires_in': 3600, 'access_token': token}
        payload = {
            "client_id": os.environ["LIBCAL_CLIENT_ID"],
            "client_secret": os.environ["LIBCAL_CLIENT_SECRET"],
            "grant_type": "client_credentials"
        }

        def match_request_payload(request):
            # parse_qs will return each value as a list (even if one item), so just leave the item.
            return payload == {k: v[0] for k, v in parse.parse_qs(request.body).items() if len(v) == 1}

        m.register_uri(
            'POST',
            f'{os.environ["LIBCAL_BASE_URL"]}/1.1/oauth/token',
            additional_matcher=match_request_payload,
            complete_qs=True,
            status_code=200,
            json=response
        )
        call_command('refresh_libcal_token')
        self.assertTrue(self.r.exists("libcal:token"))
        self.assertEqual(self.r.get("libcal:token"), token)
        self.assertEqual(self.r.delete("libcal:token"), 1)

    def test_error_handled_gracefully(self, m):
        """Test a non-200 response from LibCal is handled correctly."""
        m.register_uri(
            'POST',
            f'{os.environ["LIBCAL_BASE_URL"]}/1.1/oauth/token',
            status_code=500
        )
        self.assertRaises(SystemExit, call_command, 'refresh_libcal_token')  # Failure


@requests_mock.Mocker()
class LibCalRequestForwarderTestCase(TestCase):
    """Tests specific functionality of the _libcal_request_forwarder() function"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.r: redis.Redis = redis.Redis(
            host=REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        cls.client: APIClient = APIClient()
        cls.user_ = User.objects.create(cn="test", employee_id=7357)
        cls.app = App.objects.create(user=cls.user_, name="An App")
        cls.token: str = "random-token"
        cls.headers: dict = {
            "Authorization": f"Bearer {cls.token}"
        }
        cls.r.set("libcal:token", cls.token)

    @classmethod
    def tearDownClass(cls):
        cls.r.delete("libcal:token")
        super().tearDownClass()

    def test_no_libcal_token(self, m):
        """Test if lack of LibCal OAuth token in Redis is handled gracefully."""
        self.r.delete("libcal:token")
        expected_json = {
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }
        response = self.client.get('/libcal/space/locations', {'token': self.app.api_token})
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content.decode("utf-8"), expected_json)

    def test_unauthorized(self, m):
        '''Tests that we correctly handle a 401 Unauthorized from LibCal'''
        expected_json = {
            "ok": False,
            "error": "Unable to refresh LibCal OAuth token"
        }
        m.register_uri(
            'GET',
            'https://library-calendars.ucl.ac.uk/1.1/space/locations',
            request_headers=self.headers,
            status_code=401)
        response = self.client.get('/libcal/space/locations', {'token': self.app.api_token})
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content.decode("utf-8"), expected_json)


@requests_mock.Mocker()
class LibcalNonPersonalEndpointsTestCase(TestCase):
    """Tests for LibCal endpoints that don't display personal data."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # We prefer client to factory as we want to test if
        # the regex is correct as well.
        cls.client: APIClient = APIClient()
        cls.user_ = User.objects.create(cn="test", employee_id=7357)
        cls.app = App.objects.create(user=cls.user_, name="An App")
        cls.token: str = "random-token"
        cls.headers: dict = {
            "Authorization": f"Bearer {cls.token}"
        }
        cls.r: redis.Redis = redis.Redis(
            host=REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        cls.r.set("libcal:token", cls.token)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.r.delete("libcal:token")

    @parameterized.expand([('locations')])
    def test_token_is_checked(self, m, uclapi_endpoint):
        """Tests that we check for a valid UCL API token"""
        # NOTE: token isn't sent in!
        response = self.client.get(f'/libcal/space/{uclapi_endpoint}')
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('locations', '1.1/space/locations', 'details', 0),
        ('locations', '1.1/space/locations', 'details', 1)
    ], name_func=all_params_except_libcal_endpoint)
    def test_serializer_valid_input(self, m, uclapi_endpoint, libcal_endpoint, key, value):
        """Tests that GET parameters are validated"""
        json = {'key': 'value'}
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/{libcal_endpoint}?{key}={value}',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token is sent in!
            json=json)
        response = self.client.get(f'/libcal/space/{uclapi_endpoint}', {key: value, 'token': self.app.api_token})
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('locations', 'details', 0.5),
        ('locations', 'details', -1),
        ('locations', 'details', 2),
        ('locations', 'details', ';DROP table;--')
    ], name_func=all_params)
    def test_serializer_invalid_input(self, m, uclapi_endpoint, key, value):
        """Tests that invalid GET parameters are caught"""
        response = self.client.get(f'/libcal/space/{uclapi_endpoint}', {key: value, 'token': self.app.api_token})
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('locations', '1.1/space/locations', 'admin_only', 1)
    ], name_func=all_params_except_libcal_endpoint)
    def test_serializer_blacklisted_input(self, m, uclapi_endpoint, libcal_endpoint, key, value):
        """Tests that blacklisted GET parameters are not sent to LibCal"""
        json = {'key': 'value'}
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/{libcal_endpoint}',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token or blacklisted input is sent in!
            json=json)
        response = self.client.get(f'/libcal/space/{uclapi_endpoint}', {key: value, 'token': self.app.api_token})
        self.assertEqual(response.status_code, 200)
