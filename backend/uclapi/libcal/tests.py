import json
import os
from unittest import mock
from urllib import parse

import redis
import requests_mock
from celery.exceptions import Ignore
from parameterized import parameterized
from rest_framework.test import APISimpleTestCase, APITestCase, APIClient

from dashboard.models import App, User
from oauth.models import OAuthScope, OAuthToken
from oauth.scoping import Scopes
from uclapi.settings import REDIS_UCLAPI_HOST
from .tasks import refresh_libcal_token
from .utils import underscore


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
        refresh_libcal_token()
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
        self.assertRaises(Ignore, refresh_libcal_token)


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
        cls.user_ = User.objects.create(cn="test", employee_id=7357, dev_quota=9999999)
        cls.app = App.objects.create(user=cls.user_, name="An App")
        cls.token: str = "random-token"
        cls.headers: dict = {
            "Authorization": f"Bearer {cls.token}"
        }
        cls.r.set("libcal:token", cls.token)

    def setUp(self):
        self.r.set("libcal:token", self.token)

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

    def test_non_json_response(self, m):
        """Tests that we correctly handle non-JSON non-200 response.

        Note that we only check if the response is JSON for non-200 responses.
        We assume the response is JSON if it is a 200 (would be VERY surprising if it wasn't...)"""
        expected_json = {
            "ok": False,
            "error": "LibCal endpoint did not return a JSON response."
        }
        m.register_uri(
            'GET',
            'https://library-calendars.ucl.ac.uk/1.1/space/locations',
            request_headers=self.headers,
            text='Lot of non-JSON text!',
            status_code=404)
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
        cls.user_ = User.objects.create(cn="test", employee_id=7357, dev_quota=9999999)
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
        cls.r.delete("libcal:token")
        super().tearDownClass()

    @parameterized.expand([('locations'), ('form?ids=1'), ('question?ids=1'), ('categories?ids=1'), ('category?ids=1'),
                           ('item?ids=1'), ('nickname?ids=1'), ('utilization?ids=1'), ('seat?ids=1'), ('seats?ids=1'),
                           ('zone?ids=1'), ('zones?ids=1'), ('bookings')])
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
        ('seats', 'api/1.1/space/seats/1', 'pageSize', 99),
        ('bookings', '1.1/space/bookings', 'eid', 123),
        ('bookings', '1.1/space/bookings', 'eid', '12,345'),
        ('bookings', '1.1/space/bookings', 'seat_id', 123),
        ('bookings', '1.1/space/bookings', 'seat_id', '12,345'),
        ('bookings', '1.1/space/bookings', 'cid', 123),
        ('bookings', '1.1/space/bookings', 'cid', '12,345'),
        ('bookings', '1.1/space/bookings', 'lid', 123),
        ('bookings', '1.1/space/bookings', 'date', '2021-01-01'),
        ('bookings', '1.1/space/bookings', 'limit', 1),
        ('bookings', '1.1/space/bookings', 'limit', 500)
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
            {'ids': 1, underscore(key): value, 'token': self.app.api_token}
        )
        self.assertEqual(response.status_code, 200)

    def test_bookings_personal_information_stripped(self, m):
        """Tests that personal information is stripped from the booking"""
        allowed_fields = ['seat_name']
        json = [{'email': 'delete_me', 'firstName': 'delete_me', 'lastName': 'delete_me',
                 'bookId': 'delete_me', 'check_in_code': 'delete_me', 'seat_name': 'leave_me',
                 'random_unknown_key': 'delete_me'}]
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/bookings?eid=123',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token is sent in!
            json=json)
        response = self.client.get(
            f'/libcal/space/bookings',
            {'ids': 1, 'eid': 123, 'token': self.app.api_token}
        )

        # Make sure the number of fields in the returned booking that are not in allowed_fields is 0
        for booking in response.json()['bookings']:
            self.assertEqual(len([x for x in booking.keys() if x not in allowed_fields]), 0)

        for k, v in response.json()['bookings'][0].items():
            self.assertEqual(k, 'seat_name')
            self.assertEqual(v, 'leave_me')

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
        ('seats', 'pageSize', ';DROP table;--'),
        ('bookings', 'eid', ';DROP table;--'),
        ('bookings', 'eid', '-4'),
        ('bookings', 'eid', '23.5'),
        ('bookings', 'eid', '47,,4'),
        ('bookings', 'eid', ','),
        ('bookings', 'eid', '1,2.3'),
        ('bookings', 'eid', '8,'),
        ('bookings', 'seat_id', ';DROP table;--'),
        ('bookings', 'seat_id', '-4'),
        ('bookings', 'seat_id', '23.5'),
        ('bookings', 'seat_id', '47,,4'),
        ('bookings', 'seat_id', ','),
        ('bookings', 'seat_id', '1,2.3'),
        ('bookings', 'seat_id', '8,'),
        ('bookings', 'cid', ';DROP table;--'),
        ('bookings', 'cid', '-4'),
        ('bookings', 'cid', '23.5'),
        ('bookings', 'cid', '47,,4'),
        ('bookings', 'cid', ','),
        ('bookings', 'cid', '1,2.3'),
        ('bookings', 'cid', '8,'),
        ('bookings', 'lid', ';DROP table;--'),
        ('bookings', 'lid', '-4'),
        ('bookings', 'lid', '23.5'),
        ('bookings', 'lid', '47,,4'),
        ('bookings', 'lid', ','),
        ('bookings', 'lid', '1,2.3'),
        ('bookings', 'lid', '8,'),
        ('bookings', 'date', ';DROP table;--'),
        ('bookings', 'date', '2021'),
        ('bookings', 'date', '2021-01'),
        ('bookings', 'date', '2021-01-01T:00:00:00'),
        ('bookings', 'date', '2021-01-01T:00:00:00+00:00'),
        ('bookings', 'limit', 0),
        ('bookings', 'limit', 501),
        ('bookings', 'limit', ';DROP table;--')
    ], name_func=all_params)
    def test_serializer_invalid_input(self, m, uclapi_endpoint, key, value):
        """Tests that invalid GET parameters are caught"""
        response = self.client.get(
            f'/libcal/space/{uclapi_endpoint}',
            {'ids': 1, underscore(key): value, 'token': self.app.api_token}
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
        ("zone", "api/1.1/space/zone", 'zone'),
        ("zones", "api/1.1/space/zones", 'zones')
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
                           ('utilization'), ('seat'), ('seats'), ('zone'), ('zones')])
    def test_invalid_id_list(self, m, endpoint):
        """Tests that invalid format of ID(s) is not proxied and is caught by us."""
        valid_ids: list[str] = ["hello", "-4", "23.5", "47,,4", ",", "1,2.3", "8,"]
        for id in valid_ids:
            response = self.client.get(f'/libcal/space/{endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 400)

    @parameterized.expand([('utilization'), ('seat'), ('seats'), ('zone'), ('zones')])
    def test_id_list_returns_404(self, m, endpoint):
        """Tests that a valid list of IDs is not proxied and is caught by us.

        Some endpoints do not accept a list, only one ID.
        This is primarily a test of the regex in urls.py
        """
        valid_ids: list[str] = ["1,2", "12,345", "12,03456789"]
        for id in valid_ids:
            response = self.client.get(f'/libcal/space/{endpoint}', {'ids': id, 'token': self.app.api_token})
            self.assertEqual(response.status_code, 400)


@requests_mock.Mocker()
@mock.patch.dict(os.environ, {"LIBCAL_BASE_URL": "https://library-calendars.ucl.ac.uk"})
class LibcalPersonalEndpointsTestCase(APITestCase):
    """Tests for LibCal endpoints that display personal data."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create User, App, and OAuth it
        cls.user = User.objects.create(
            email='zc@ucl.ac.uk', cn="test", employee_id=7357, mail='f.l.2021@ucl.ac.uk', given_name='John', sn='Doe'
        )
        cls.app_dev = User.objects.create(cn="test2", employee_id=1122)
        cls.app: App = App.objects.create(user=cls.app_dev, name="An App")
        cls.scopes_class = Scopes()
        cls.oauth_scope = OAuthScope.objects.create(scope_number=0)
        cls.oauth_token = OAuthToken.objects.create(
            app=cls.app,
            user=cls.user,
            scope=cls.oauth_scope
        )
        cls.libcal_token: str = "random-token"
        cls.headers: dict = {
            "Authorization": f"Bearer {cls.libcal_token}"
        }
        cls.r: redis.Redis = redis.Redis(
            host=REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        cls.r.set("libcal:token", cls.libcal_token)

    @classmethod
    def tearDownClass(cls):
        cls.r.delete("libcal:token")
        super().tearDownClass()

    def setUp(self):
        # Some tests change this value during testing.
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, '')
        self.oauth_token.scope.save()
        self.user.mail = 'f.l.2021@ucl.ac.uk'
        self.user.email = 'zc@ucl.ac.uk'
        self.user.save()

    @parameterized.expand([
        ('personal_bookings', 'GET', ''),
        ('reserve', 'POST', ''),
        ('cancel', 'POST', 'cs_qQpoVMHk')
    ])
    def test_non_personal_token_rejected(self, m, endpoint, method, bookIds):
        """Tests that we reject a non-personal data token"""
        if method == 'GET':
            response = self.client.get(
                f'/libcal/space/{endpoint}',
                {'token': self.app.api_token, 'client_secret': self.app.client_secret, 'ids': bookIds}
            )
        else:
            response = self.client.post(
                f'/libcal/space/{endpoint}',
                {'token': self.app.api_token, 'client_secret': self.app.client_secret, 'ids': bookIds},
                format='json'
            )
        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('personal_bookings', 'libcal_read', 'GET', ''),
        ('reserve', 'libcal_write', 'POST', ''),
        ('cancel', 'libcal_write', 'POST', 'cs_qQpoVMHk')
    ])
    def test_lack_of_client_secret_rejected(self, m, endpoint, scope, method, bookIds):
        """Tests that we reject an read OAuth token presented without a client secret"""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, scope)
        self.oauth_token.scope.save()
        if method == 'GET':
            response = self.client.get(
                f'/libcal/space/{endpoint}', {'token': self.oauth_token.token, 'ids': bookIds})
        else:
            response = self.client.post(
                f'/libcal/space/{endpoint}', {'token': self.oauth_token.token, 'ids': bookIds}, format='json')

        self.assertEqual(response.status_code, 400)

    @parameterized.expand([
        ('personal_bookings', 'libcal_read', 'GET', ''),
        ('reserve', 'libcal_write', 'POST', ''),
        ('cancel', 'libcal_write', 'POST', 'cs_qQpoVMHk')
    ])
    def test_wrong_scope_rejected(self, m, endpoint, correct_scope, method, bookIds):
        """Tests that we reject an OAuth token presented with the wrong scope"""
        # NOTE: scope is currently '' (0)
        if method == 'GET':
            response = self.client.get(
                f'/libcal/space/{endpoint}',
                {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, 'ids': bookIds}
            )
        else:
            response = self.client.post(
                f'/libcal/space/{endpoint}',
                {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, 'ids': bookIds},
                format='json'
            )
        self.assertEqual(response.status_code, 400)

        for scope in self.scopes_class.SCOPE_MAP:
            if scope == correct_scope:
                continue
            self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, scope)
            self.oauth_token.scope.save()
            if method == 'GET':
                response = self.client.get(
                    f'/libcal/space/{endpoint}',
                    {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, 'ids': bookIds}
                )
            else:
                response = self.client.post(
                    f'/libcal/space/{endpoint}',
                    {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, 'ids': bookIds}
                )
            self.assertEqual(response.status_code, 400)

    def test_lack_of_email_caught(self, m):
        """Tests that we error out when the email is empty"""
        self.user.mail = ''
        self.user.email = ''
        self.user.save()
        response = self.client.get(
            '/libcal/space/personal_bookings',
            {'token': self.oauth_token.token, 'client_secret': self.app.client_secret}
        )
        self.assertEqual(response.status_code, 400)

    def test_bookings_list(self, m):
        """Test that a valid call to the personal_bookings endpoint results in a 200 response."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_read')
        self.oauth_token.scope.save()
        json = {'key': 'value'}
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/bookings?email={self.user.mail}',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token is sent in!
            json=json)
        response = self.client.get(
            '/libcal/space/personal_bookings',
            {'token': self.oauth_token.token, 'client_secret': self.app.client_secret}
        )
        self.assertEqual(response.status_code, 200)

    def test_bookings_fallback(self, m):
        """Tests that we fallback to eppn if mail is empty."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_read')
        self.oauth_token.scope.save()
        self.user.mail = ''
        self.user.save()
        json = {'key': 'value'}
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/bookings?email={self.user.email}',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token is sent in!
            json=json)
        response = self.client.get(
            '/libcal/space/personal_bookings',
            {'token': self.oauth_token.token, 'client_secret': self.app.client_secret}
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('eid', 123),
        ('eid', '12,345'),
        ('seat_id', 123),
        ('seat_id', '12,345'),
        ('cid', 123),
        ('cid', '12,345'),
        ('lid', 123),
        ('date', '2021-01-01'),
        ('limit', 1),
        ('limit', 500),
        ('formAnswers', 0),
        ('formAnswers', 1)
    ], name_func=all_params_except_libcal_endpoint)
    def test_serializer_valid_input(self, m, key, value):
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_read')
        self.oauth_token.scope.save()
        json = {'key': 'value'}
        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/bookings?email={self.user.mail}&{key}={value}',
            request_headers=self.headers,
            complete_qs=True,  # Need this to catch if token is sent in!
            json=json)
        response = self.client.get(
            '/libcal/space/personal_bookings',
            {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, underscore(key): value}
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('eid', ';DROP table;--'),
        ('eid', '-4'),
        ('eid', '23.5'),
        ('eid', '47,,4'),
        ('eid', ','),
        ('eid', '1,2.3'),
        ('eid', '8,'),
        ('seat_id', ';DROP table;--'),
        ('seat_id', '-4'),
        ('seat_id', '23.5'),
        ('seat_id', '47,,4'),
        ('seat_id', ','),
        ('seat_id', '1,2.3'),
        ('seat_id', '8,'),
        ('cid', ';DROP table;--'),
        ('cid', '-4'),
        ('cid', '23.5'),
        ('cid', '47,,4'),
        ('cid', ','),
        ('cid', '1,2.3'),
        ('cid', '8,'),
        ('lid', ';DROP table;--'),
        ('lid', '-4'),
        ('lid', '23.5'),
        ('lid', '47,,4'),
        ('lid', ','),
        ('lid', '1,2.3'),
        ('lid', '8,'),
        ('date', ';DROP table;--'),
        ('date', '2021'),
        ('date', '2021-01'),
        ('date', '2021-01-01T:00:00:00'),
        ('date', '2021-01-01T:00:00:00+00:00'),
        ('limit', 0),
        ('limit', 501),
        ('limit', ';DROP table;--'),
        ('formAnswers', ';DROP table;--'),
        ('formAnswers', 0.5),
        ('formAnswers', -1)
    ])
    def test_serializer_invalid_input(self, m, key, value):
        response = self.client.get(
            '/libcal/space/personal_bookings',
            {'token': self.oauth_token.token, 'client_secret': self.app.client_secret, underscore(key): value}
        )
        self.assertEqual(response.status_code, 400)

    def test_reserve(self, m):
        """Test that the reserve endpoint accepts valid payloads."""
        payload = {
            "start": "2021-02-22T13:00:00",
            "test": 1,
            "bookings": [
                {
                    "id": 12102,
                    "seat_id": 63610,
                    "to": "2021-02-22T16:30:00"
                }
            ]
        }

        def match_request_payload(request):
            data = json.loads(request.body.decode('utf8'))
            payload['email'] = self.user.mail
            payload['fname'] = self.user.given_name
            payload['lname'] = self.user.sn
            return data == payload

        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        resp = {'key': 'value'}
        m.register_uri(
            'POST',
            'https://library-calendars.ucl.ac.uk/1.1/space/reserve',
            request_headers=self.headers,
            additional_matcher=match_request_payload,  # TODO
            complete_qs=True,  # Need this to catch if token is sent in!
            json=resp)
        response = self.client.post(
            f'/libcal/space/reserve?token={self.oauth_token.token}&client_secret={self.app.client_secret}',
            payload, format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_reserve_multiple_bookings(self, m):
        payload = {
            "start": "2021-02-22T13:00:00",
            "test": 1,
            "bookings": [
                {
                    "id": 12102,
                    "seat_id": 63610,
                    "to": "2021-02-22T16:30:00"
                },
                {
                    "id": 12103,
                    "seat_id": 63610,
                    "to": "2021-02-22T16:30:00"
                }
            ]
        }

        def match_request_payload(request):
            data = json.loads(request.body.decode('utf8'))
            payload['email'] = self.user.mail
            payload['fname'] = self.user.given_name
            payload['lname'] = self.user.sn
            return data == payload

        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        resp = {'key': 'value'}
        m.register_uri(
            'POST',
            'https://library-calendars.ucl.ac.uk/1.1/space/reserve',
            request_headers=self.headers,
            additional_matcher=match_request_payload,  # TODO
            complete_qs=True,  # Need this to catch if token is sent in!
            json=resp)
        response = self.client.post(
            f'/libcal/space/reserve?token={self.oauth_token.token}&client_secret={self.app.client_secret}',
            payload, format='json'
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('2021-02-22T13:00:00+00:00', 1, 2, 3, ';DROP table;--'),
        ('2021-02-22T13:00:00+00:00', 1, 2, 3, '2021-02-22'),
        ('2021-02-22T13:00:00+00:00', 1, 2, -1, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', 1, 2, ';DROP table;--', '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', 1, -1, 3, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', 1, ';DROP table;--', 3, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', -1, 2, 3, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', 2, 2, 3, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22T13:00:00+00:00', ';DROP table;--', 2, 3, '2021-02-22T13:00:00+00:00'),
        (';DROP table;--', 1, 2, 3, '2021-02-22T13:00:00+00:00'),
        ('2021-02-22', 1, 2, 3, '2021-02-22T13:00:00+00:00')
    ])
    def test_post_serializer_invalid_input(self, m, start, test, id, seat_id, to):
        """Test that the reserve POST serializer does not pass on invalid payloads."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        payload = {
            "start": start,
            "test": test,
            "bookings": [
                {
                    "id": id,
                    "seat_id": seat_id,
                    "to": to
                }
            ]
        }
        response = self.client.post(
            f'/libcal/space/reserve?token={self.oauth_token.token}&client_secret={self.app.client_secret}',
            payload, format='json'
        )
        self.assertEqual(response.status_code, 400)

    def test_reserve_adminbooking_blacklisted(self, m):
        """Tests that the adminbooking parameter is not sent to LibCal"""
        payload = {
            "start": "2021-02-22T13:00:00",
            "test": 1,
            "adminbooking": 1,
            "bookings": [
                {
                    "id": 12102,
                    "seat_id": 63610,
                    "to": "2021-02-22T16:30:00"
                }
            ]
        }

        def match_request_payload(request):
            data = json.loads(request.body.decode('utf8'))
            payload['email'] = self.user.mail
            payload['fname'] = self.user.given_name
            payload['lname'] = self.user.sn
            payload.pop("adminbooking", None)
            return data == payload

        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        resp = {'key': 'value'}
        m.register_uri(
            'POST',
            'https://library-calendars.ucl.ac.uk/1.1/space/reserve',
            request_headers=self.headers,
            additional_matcher=match_request_payload,  # TODO
            complete_qs=True,  # Need this to catch if token is sent in!
            json=resp)
        response = self.client.post(
            f'/libcal/space/reserve?token={self.oauth_token.token}&client_secret={self.app.client_secret}',
            payload, format='json'
        )
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(['cs_qQpoVMHk', 'cs_qQpoVMHk,cs_qQpoRH20'])
    def test_valid_cancel(self, m, bookIds):
        """Tests that a valid id or a list of valid ids is cancelled by LibCal."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        bookings = []
        cancelled = []
        for bookId in bookIds.split(','):
            bookings.append({'email': self.user.mail, 'bookId': bookId})
            cancelled.append({'booking_id': bookId, 'cancelled': True})

        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/booking/{bookIds}',
            request_headers=self.headers,
            json=bookings)
        m.register_uri(
            'POST',
            f'https://library-calendars.ucl.ac.uk/1.1/space/cancel/{bookIds}',
            request_headers=self.headers,
            json=cancelled)
        response = self.client.post(
            f'/libcal/space/cancel?ids={bookIds}&token={self.oauth_token.token}&client_secret={self.app.client_secret}'
        )
        self.assertEqual(response.status_code, 200)
        # https://stackoverflow.com/a/28399670
        self.assertJSONEqual(response.content.decode('utf8'), {"ok": True, 'bookings': cancelled})

    @parameterized.expand(['cs_qQpoVMHk', 'cs_qQpoVMHk,cs_qQpoRH20'])
    def test_cancel_ignore_invalid_id(self, m, bookIds):
        """Tests that only valid bookings belonging to the user are deleted."""
        valid_booking = 'cs_qQpoVMHk'
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        bookings = [{'email': self.user.mail, 'bookId': valid_booking}]
        cancelled = []
        for bookId in bookIds.split(','):
            if bookId == valid_booking:
                cancelled.append({'booking_id': bookId, 'cancelled': True})

        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/booking/{bookIds}',
            request_headers=self.headers,
            json=bookings)
        m.register_uri(
            'POST',
            f'https://library-calendars.ucl.ac.uk/1.1/space/cancel/{valid_booking}',
            request_headers=self.headers,
            json=cancelled)
        response = self.client.post(
            f'/libcal/space/cancel?ids={bookIds}&token={self.oauth_token.token}&client_secret={self.app.client_secret}'
        )
        self.assertEqual(response.status_code, 200)
        # https://stackoverflow.com/a/28399670
        self.assertJSONEqual(response.content.decode('utf8'), {"ok": True, 'bookings': cancelled})

    @parameterized.expand(['cs_qQpoVMHk', 'cs_qQpoVMHk,cs_qQpoRH20'])
    def test_cancel_reject_other_user_booking(self, m, bookIds):
        """Tests that only valid bookings belonging to the user are deleted."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        bookings = [{'email': 'not.this.user@example.com', 'bookId': 'cs_qQpoVMHk'}]

        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/booking/{bookIds}',
            request_headers=self.headers,
            json=bookings)
        response = self.client.post(
            f'/libcal/space/cancel?ids={bookIds}&token={self.oauth_token.token}&client_secret={self.app.client_secret}'
        )
        self.assertEqual(response.status_code, 400)
        # https://stackoverflow.com/a/28399670
        self.assertJSONEqual(response.content.decode('utf8'), {"ok": False,
                                                               "error": "No bookings matched the IDs provided and "
                                                                        "so no bookings were deleted"})

    @parameterized.expand(['cs_qQpoVMHk', 'cs_qQpoVMHk,cs_qQpoRH20'])
    def test_valid_cancel_only_eppn(self, m, bookIds):
        """Tests that it is possible to cancel bookings with an empty mail but with a valid eppn."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        self.user.mail = ''
        self.user.save()
        bookings = []
        cancelled = []
        for bookId in bookIds.split(','):
            bookings.append({'email': self.user.email, 'bookId': bookId})
            cancelled.append({'booking_id': bookId, 'cancelled': True})

        m.register_uri(
            'GET',
            f'https://library-calendars.ucl.ac.uk/1.1/space/booking/{bookIds}',
            request_headers=self.headers,
            json=bookings)
        m.register_uri(
            'POST',
            f'https://library-calendars.ucl.ac.uk/1.1/space/cancel/{bookIds}',
            request_headers=self.headers,
            json=cancelled)
        response = self.client.post(
            f'/libcal/space/cancel?ids={bookIds}&token={self.oauth_token.token}&client_secret={self.app.client_secret}'
        )
        self.assertEqual(response.status_code, 200)
        # https://stackoverflow.com/a/28399670
        self.assertJSONEqual(response.content.decode('utf8'), {"ok": True, 'bookings': cancelled})

    def test_valid_cancel_empty_email(self, m):
        """Tests that we error out correctly when the user has no email address."""
        self.oauth_token.scope.scope_number = self.scopes_class.add_scope(0, 'libcal_write')
        self.oauth_token.scope.save()
        self.user.mail = ''
        self.user.email = ''
        self.user.save()
        bookId = 'cs_qQpoVMHk'
        response = self.client.post(
            f'/libcal/space/cancel?ids={bookId}&token={self.oauth_token.token}&client_secret={self.app.client_secret}'
        )
        self.assertEqual(response.status_code, 500)
        # https://stackoverflow.com/a/28399670
        self.assertJSONEqual(
            response.content.decode('utf8'),
            {
                "ok": False,
                'error': 'This booking cannot be cancelled as this user has no valid email address.'
            }
        )
