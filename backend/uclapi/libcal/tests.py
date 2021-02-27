import os
from unittest import mock
from urllib import parse

from django.core.management import call_command
from parameterized import parameterized

from rest_framework.test import APISimpleTestCase, APITestCase, APIClient
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
class LibCalManagementCommandTestCase(APISimpleTestCase):
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
@mock.patch.dict(os.environ, {"LIBCAL_BASE_URL": "https://library-calendars.ucl.ac.uk"})
class LibCalRequestForwarderTestCase(APITestCase):
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
@mock.patch.dict(os.environ, {"LIBCAL_BASE_URL": "https://library-calendars.ucl.ac.uk"})
class LibcalNonPersonalEndpointsTestCase(APITestCase):
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

    @parameterized.expand([('locations'), ('form?ids=1'), ('question?ids=1'), ('categories?ids=1'), ('category?ids=1'),
                           ('item?ids=1'), ('nickname?ids=1'), ('utilization?ids=1'), ('seat?ids=1'), ('seats?ids=1'),
                           ('zone?ids=1')])
    def test_token_is_checked(self, m, uclapi_endpoint):
        """Tests that we check for a valid UCL API token"""
        # NOTE: token isn't sent in!
        response = self.client.get(f'/libcal/space/{uclapi_endpoint}')
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('locations', '1.1/space/locations', 'details', 0),
        ('locations', '1.1/space/locations', 'details', 1),
        ('category', '1.1/space/category/1', 'details', 0),
        ('category', '1.1/space/category/1', 'details', 1),
        ('category', '1.1/space/category/1', 'availability', 'next'),
        ('category', '1.1/space/category/1', 'availability', '2021-01-01'),
        ('category', '1.1/space/category/1', 'availability', '2021-01-01,2021-01-02'),
        ('item', '1.1/space/item/1', 'availability', 'next'),
        ('item', '1.1/space/item/1', 'availability', '2021-01-01'),
        ('item', '1.1/space/item/1', 'availability', '2021-01-01,2021-01-02'),
        ('nickname', '1.1/space/nickname/1', 'date', '2021-01-01'),
        ('utilization', 'api/1.1/space/utilization/1', 'categoryId', 123),
        ('utilization', 'api/1.1/space/utilization/1', 'zoneId', 123),
        ('seat', 'api/1.1/space/seat/1', 'availability', '2021-01-01'),
        ('seat', 'api/1.1/space/seat/1', 'availability', '2021-01-01,2021-01-02'),
        ('seats', 'api/1.1/space/seats/1', 'spaceId', 123),
        ('seats', 'api/1.1/space/seats/1', 'categoryId', 123),
        ('seats', 'api/1.1/space/seats/1', 'seatId', 123),
        ('seats', 'api/1.1/space/seats/1', 'zoneId', 123),
        ('seats', 'api/1.1/space/seats/1', 'accessibleOnly', 1),
        ('seats', 'api/1.1/space/seats/1', 'availability', '2021-01-01'),
        ('seats', 'api/1.1/space/seats/1', 'availability', '2021-01-01,2021-01-02'),
        ('seats', 'api/1.1/space/seats/1', 'pageIndex', 123),
        ('seats', 'api/1.1/space/seats/1', 'pageSize', 99)
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
        response = self.client.get(
            f'/libcal/space/{uclapi_endpoint}',
            {'ids': 1, key: value, 'token': self.app.api_token}
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('locations', 'details', 0.5),
        ('locations', 'details', -1),
        ('locations', 'details', 2),
        ('locations', 'details', ';DROP table;--'),
        ('category', 'details', 0.5),
        ('category', 'details', -1),
        ('category', 'details', 2),
        ('category', 'details', ';DROP table;--'),
        ('category', 'availability', ';DROP table;--'),
        ('category', 'availability', '1next1'),
        ('category', 'availability', '2021'),
        ('category', 'availability', '2021-01'),
        ('category', 'availability', '2021-01-01,'),
        ('category', 'availability', '2021-01-01T:00:00:00'),
        ('category', 'availability', '2021-01-01T:00:00:00+00:00'),
        ('item', 'availability', ';DROP table;--'),
        ('item', 'availability', '1next1'),
        ('item', 'availability', '2021'),
        ('item', 'availability', '2021-01'),
        ('item', 'availability', '2021-01-01,'),
        ('item', 'availability', '2021-01-01T:00:00:00'),
        ('item', 'availability', '2021-01-01T:00:00:00+00:00'),
        ('nickname', 'date', ';DROP table;--'),
        ('nickname', 'date', '2021'),
        ('nickname', 'date', '2021-01'),
        ('nickname', 'date', '2021-01-01T:00:00:00'),
        ('nickname', 'date', '2021-01-01T:00:00:00+00:00'),
        ('utilization', 'categoryId', 0.5),
        ('utilization', 'categoryId', -1),
        ('utilization', 'categoryId', ';DROP table;--'),
        ('utilization', 'zoneId', 0.5),
        ('utilization', 'zoneId', -1),
        ('utilization', 'zoneId', ';DROP table;--'),
        ('seat', 'availability', ';DROP table;--'),
        ('seat', 'availability', 'next'),
        ('seat', 'availability', '2021'),
        ('seat', 'availability', '2021-01'),
        ('seat', 'availability', '2021-01-01,'),
        ('seat', 'availability', '2021-01-01T:00:00:00'),
        ('seat', 'availability', '2021-01-01T:00:00:00+00:00'),
        ('seats', 'spaceId', 0.5),
        ('seats', 'spaceId', -1),
        ('seats', 'spaceId', ';DROP table;--'),
        ('seats', 'categoryId', 0.5),
        ('seats', 'categoryId', -1),
        ('seats', 'categoryId', ';DROP table;--'),
        ('seats', 'seatId', 0.5),
        ('seats', 'seatId', -1),
        ('seats', 'seatId', ';DROP table;--'),
        ('seats', 'zoneId', 0.5),
        ('seats', 'zoneId', -1),
        ('seats', 'zoneId', ';DROP table;--'),
        ('seats', 'accessibleOnly', 0.5),
        ('seats', 'accessibleOnly', -1),
        ('seats', 'accessibleOnly', 2),
        ('seats', 'accessibleOnly', ';DROP table;--'),
        ('seats', 'availability', ';DROP table;--'),
        ('seats', 'availability', 'next'),
        ('seats', 'availability', '2021'),
        ('seats', 'availability', '2021-01'),
        ('seats', 'availability', '2021-01-01,'),
        ('seats', 'availability', '2021-01-01T:00:00:00'),
        ('seats', 'availability', '2021-01-01T:00:00:00+00:00'),
        ('seats', 'pageIndex', 0.5),
        ('seats', 'pageIndex', -1),
        ('seats', 'pageIndex', ';DROP table;--'),
        ('seats', 'pageSize', 0.5),
        ('seats', 'pageSize', 0),
        ('seats', 'pageSize', 101),
        ('seats', 'pageSize', ';DROP table;--')
    ], name_func=all_params)
    def test_serializer_invalid_input(self, m, uclapi_endpoint, key, value):
        """Tests that invalid GET parameters are caught"""
        response = self.client.get(
            f'/libcal/space/{uclapi_endpoint}',
            {'ids': 1, key: value, 'token': self.app.api_token}
        )
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('form', '1.1/space/form', 'forms'),
        ("question", "1.1/space/question", 'questions'),
        ("categories", "1.1/space/categories", 'categories'),
        ("category", "1.1/space/category", 'categories'),
        ("item", "1.1/space/item", 'items'),
        ("nickname", "1.1/space/nickname", 'nicknames'),
        ("utilization", "api/1.1/space/utilization", 'data'),
        ("seat", "api/1.1/space/seat", 'seat'),
        ("seats", "api/1.1/space/seats", 'seats'),
        ("zone", "api/1.1/space/zone", 'zone')
    ])
    def test_valid_id(self, m, uclapi_endpoint, libcal_endpoint, key):
        """Tests that a valid id is forwarded to LibCal.

        This is primarily a test of the regex in urls.py
        """
        valid_ids: list[str] = ["0", "40", "040", "1234567890"]
        json = {"data": "Doesn't matter for this test"}
        for id in valid_ids:
            m.register_uri(
                'GET',
                f'https://library-calendars.ucl.ac.uk/{libcal_endpoint}/{id}',
                request_headers=self.headers,
                json=json)
            response = self.client.get(f'/libcal/space/{uclapi_endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 200)
            # https://stackoverflow.com/a/28399670
            self.assertJSONEqual(response.content.decode('utf8'), {"ok": True, key: json})

    @parameterized.expand([
        ('locations', '1.1/space/locations', 'admin_only', 1),
        ('categories', '1.1/space/categories/1', 'admin_only', 1)
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

        response = self.client.get(
            f'/libcal/space/{uclapi_endpoint}',
            # Note all endpoints need ids set, but some do. No harm in setting it for all endpoints.
            # Can't simply add it into the parameterized tuple as the client will strip query params present.
            {'ids': 1, key: value, 'token': self.app.api_token}
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('form', '1.1/space/form', 'forms'),
        ("question", "1.1/space/question", 'questions'),
        ("categories", "1.1/space/categories", 'categories'),
        ("category", "1.1/space/category", 'categories'),
        ("item", "1.1/space/item", 'items'),
        ("nickname", "1.1/space/nickname", 'nicknames'),
    ])
    def test_valid_id_list(self, m, uclapi_endpoint, libcal_endpoint, key):
        """Tests that a valid id or a list of valid ids is forwarded to LibCal."""
        valid_ids: list[str] = ["1", "1,2", "12,345"]
        json = {"data": "Doesn't matter for this test"}
        for id in valid_ids:
            m.register_uri(
                'GET',
                f'https://library-calendars.ucl.ac.uk/{libcal_endpoint}/{id}',
                request_headers=self.headers,
                json=json)
            response = self.client.get(f'/libcal/space/{uclapi_endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 200)
            # https://stackoverflow.com/a/28399670
            self.assertJSONEqual(response.content.decode('utf8'), {"ok": True, key: json})

    @parameterized.expand([('form'), ('question'), ('categories'), ('category'), ('item'), ('nickname'),
                           ('utilization'), ('seat'), ('seats'), ('zone')])
    def test_invalid_id_list(self, m, endpoint):
        """Tests that invalid format of ID(s) is not proxied and is caught by us."""
        valid_ids: list[str] = ["hello", "-4", "23.5", "47,,4", ",", "1,2.3", "8,"]
        for id in valid_ids:
            response = self.client.get(f'/libcal/space/{endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 400)

    @parameterized.expand([('utilization'), ('seat'), ('seats'), ('zone')])
    def test_id_list_returns_404(self, m, endpoint):
        """Tests that a valid list of IDs is not proxied and is caught by us.

        Some endpoints do not accept a list, only one ID.
        This is primarily a test of the regex in urls.py
        """
        valid_ids: list[str] = ["1,2", "12,345", "12,03456789"]
        for id in valid_ids:
            response = self.client.get(f'/libcal/space/{endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 400)
