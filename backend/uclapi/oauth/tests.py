import json
import os
import random
import string
import unittest.mock

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.test import Client, TestCase
from django_mock_queries.query import MockModel, MockSet
from rest_framework.test import APIRequestFactory, APITestCase
from django.core import signing
from parameterized import parameterized
from requests.models import Response

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse

from dashboard.models import App, User

from .app_helpers import generate_random_verification_code
from .models import OAuthScope, OAuthToken
from .scoping import Scopes
from .views import authorise, adcallback, deauthorise_app


@uclapi_protected_endpoint(personal_data=True, required_scopes=["timetable"])
def test_timetable_request(request, *args, **kwargs):
    return JsonResponse({
        "ok": True
    }, custom_header_data=kwargs)


def unsign(data, max_age):
    raise signing.SignatureExpired


# https://stackoverflow.com/a/65437794
def mocked_adcallback_post(*args, **kwargs):
    response_content = None
    request_url = args[0].split('?')[0]

    if request_url == os.environ.get("AZURE_AD_ROOT") + "/oauth2/v2.0/token":
        response_content = json.dumps({
            'token_type': 'Bearer',
            'scope': 'Group.Read.All profile openid email User.Read',
            'expires_in': 4780,
            'ext_expires_in': 4780,
            'access_token': 'eyfoo',
            'id_token': 'eybar'
        })

    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response

def mocked_ad_graph_get(*args, **kwargs):
    response_content = None
    request_url = args[0].split('?')[0]

    if request_url == os.environ.get("AZURE_GRAPH_ROOT") + '/me':
        response_content = json.dumps(kwargs['user_data'])
    elif request_url == os.environ.get("AZURE_GRAPH_ROOT") + '/me/transitiveMemberOf':
        response_content = json.dumps({'value': kwargs['group_data']})

    response = Response()
    response.status_code = 200
    response._content = str.encode(response_content)
    return response

class ScopingTestCase(TestCase):
    test_scope_map = {
        "roombookings": (0, "Private room bookings data"),
        "timetable": (1, "Private timetable data"),
        "uclu": (2, "Private UCLU data"),
        "moodle": (3, "Private Moodle data")
    }

    def setUp(self):
        self.s = Scopes(self.test_scope_map)
        self.scope_a = OAuthScope.objects.create()
        self.scope_b = OAuthScope.objects.create()

    def test_add_scope(self):
        self.scope_a.scope_number = self.s.add_scope(
            self.scope_a.scope_number,
            "roombookings"
        )
        self.scope_a.scope_number = self.s.add_scope(
            self.scope_a.scope_number,
            "timetable"
        )
        self.scope_a.save()

        self.scope_b.scope_number = self.s.add_scope(
            self.scope_b.scope_number,
            "timetable"
        )
        self.scope_b.save()

        self.assertEqual(self.scope_a.scope_number, 3)
        self.assertEqual(self.scope_b.scope_number, 2)

    def test_add_incorrect_scope(self):
        self.scope_a.scope_number = 3
        self.scope_a.scope_number = self.s.add_scope(
            self.scope_a.scope_number,
            "blah"
        )
        self.assertEqual(self.scope_a.scope_number, 3)

    def test_remove_scope(self):
        self.scope_a.scope_number = 3
        self.scope_a.scope_number = self.s.remove_scope(
            self.scope_a.scope_number,
            "roombookings"
        )
        self.scope_a.save()

        self.assertEqual(self.scope_a.scope_number, 2)

    def test_remove_incorrect_scope(self):
        self.scope_a.scope_number = 3
        self.scope_a.scope_number = self.s.remove_scope(
            self.scope_a.scope_number,
            "blah"
        )
        self.scope_a.save()
        self.assertEqual(self.scope_a.scope_number, 3)

    def test_scopes_equal(self):
        equal = self.scope_a.scopeIsEqual(self.scope_b)

        self.assertTrue(equal)

    def test_check_scope(self):
        self.assertFalse(self.s.check_scope(12, "roombookings"))
        self.assertTrue(self.s.check_scope(12, "uclu"))

    def test_get_all_scopes(self):
        scopes_bare = self.s.get_all_scopes(pretty_print=False)
        self.assertTrue({
            "name": "roombookings",
            "id": 0
        } in scopes_bare)

        scopes_pretty = self.s.get_all_scopes(pretty_print=True)
        self.assertTrue({
            "name": "roombookings",
            "description": "Private room bookings data"
        } in scopes_pretty)

    def test_scopes_dict(self):
        scopes_dict = self.s.scope_dict(5, pretty_print=False)
        check_dict = [
            {
                "name": "roombookings",
                "id": 0
            },
            {
                "name": "uclu",
                "id": 2
            }
        ]

        scopes_dict.sort(key=lambda x: x["id"])
        check_dict.sort(key=lambda x: x["id"])
        self.assertEqual(scopes_dict, check_dict)

    def test_dump_scopes_map(self):
        scopes_map = self.s.get_scope_map()
        self.assertTrue(
            {
                "name": "roombookings",
                "id": 0,
                "description": "Private room bookings data"
            } in scopes_map
        )


class OAuthTokenCheckDecoratorTestCase(TestCase):
    def setUp(self):
        mock_status_code = unittest.mock.Mock()
        mock_status_code.status_code = 200

        self.factory = APIRequestFactory()

    def test_decorator_no_token_provided(self):
        request = self.factory.get(
            '/oauth/testcase',
            {'client_secret': 'not_a_real_secret'}
        )
        response = test_timetable_request(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No token provided.")

    def test_decorator_invalid_token_provided(self):

        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'not_a_real_secret',
                'token': 'fake'
            }
        )
        response = test_timetable_request(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Token is invalid.")

    def test_decorator_nonexistent_oauth_token_provided(self):

        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'not_a_real_secret',
                'token': 'uclapi-user-fake'
            }
        )
        response = test_timetable_request(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Token does not exist.")

    def test_decorator_client_secret_verification_failed(self):
        # create User, App, and OAuth it
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create()
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope
        )
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'not_a_real_secret',
                'token': oauth_token.token
            }
        )
        response = test_timetable_request(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Client secret incorrect."
        )

    def test_decorator_no_permission_to_access(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        oauth_scope_app = OAuthScope.objects.create(
            scope_number=0,
        )
        app_ = App.objects.create(
            user=user_,
            name="An App",
            scope=oauth_scope_app
        )
        oauth_scope_user = OAuthScope.objects.create(
            scope_number=1
        )
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope_user
        )

        request = self.factory.get(
            '/oauth/testcase',
            {
                'token': oauth_token.token,
                'client_secret': app_.client_secret
            }
        )

        response = test_timetable_request(request)
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "The token provided does not have permission"
            " to access this data."
        )

    def test_decorator_token_inactive(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create()
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope,
            active=False
        )
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': app_.client_secret,
                'token': oauth_token.token
            }
        )
        response = test_timetable_request(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            "The token is inactive as the user has revoked "
            "your app's access to their data."
        )

    def test_decorator_everything_passes(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create(
            scope_number=2
        )
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope
        )

        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': app_.client_secret,
                'token': oauth_token.token
            }
        )
        response = test_timetable_request(request)

        self.assertEqual(response.status_code, 200)

    def test_no_callback_url(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        request = self.factory.get(
            '/oauth/authorise',
            {
                'client_id': app_.client_id,
                'state': 1
            }
        )
        try:
            response = authorise(request)
            content = json.loads(response.content.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                content["error"],
                (
                    "This app does not have a callback URL set. "
                    "If you are the developer of this app, "
                    "please ensure you have set a valid callback "
                    "URL for your application in the Dashboard. "
                    "If you are a user, please contact the app's "
                    "developer to rectify this."
                )
            )
        except json.decoder.JSONDecodeError:
            self.fail("Got through to authorize page with no callback URL set")


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()

    def test_no_parameters(self):
        request = self.factory.get(
            '/oauth/authorise',
            {
            }
        )
        try:
            response = authorise(request)
            content = json.loads(response.content.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                content["error"],
                "incorrect parameters supplied"
            )
        except json.decoder.JSONDecodeError:
            self.fail("Got through to authorize page (This shouldn't happen!)")

    def test_no_app(self):
        request = self.factory.get(
            '/oauth/authorise',
            {
                'client_id': "1",
                'state': "1"
            }
        )
        try:
            response = authorise(request)
            content = json.loads(response.content.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                content["error"],
                "App does not exist for client id"
            )
        except json.decoder.JSONDecodeError:
            self.fail("Got through to authorize page (This shouldn't happen!)")

    def test_auth_flow_works(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(
            user=user_,
            name="An App",
            callback_url="www.validCallBackUrl?.com"
        )
        request = self.factory.get(
            '/oauth/authorise',
            {
                'client_id': app_.client_id,
                'state': 1
            }
        )
        k = unittest.mock.patch.dict(
            os.environ,
            {'AZURE_AD_ROOT': 'http://rooturl.com', 'AZURE_AD_CLIENT_ID': 'foo'}
        )
        k.start()
        response = authorise(request)
        k.stop()
        self.assertEqual(response.status_code, 302)

    def test_no_signed_data(self):
        request = self.factory.get(
            '/oauth/adcallback',
            {
            }
        )
        response = adcallback(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            ("No signed app data returned from Azure AD."
            " Please use the authorise endpoint.")
        )

    def test_invalid_signed_data(self):
        request = self.factory.get(
            '/oauth/adcallback',
            {
                'state': "invalid"
            }
        )
        response = adcallback(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            ("Bad signature. Please attempt to log in again. "
             "If the issues persist please contact the UCL API "
             "Team to rectify this.")
        )

    @unittest.mock.patch(
        'django.core.signing.TimestampSigner.unsign',
        side_effect=unsign
    )
    def test_expired_signature(self, TimestampSigner):
        request = self.factory.get(
            '/oauth/adcallback',
            {
                'state': "invalid"
            }
        )
        response = adcallback(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            ("Login data has expired. Please attempt to log in again. "
             "If the issues persist please contact the UCL API "
             "Team to rectify this.")
        )

    @parameterized.expand([
        ('/oauth/adcallback'),
        ('/dashboard/user/login.callback'),
        ('/settings/user/login.callback')
    ])
    def test_invalid_adcallback_real_account(self, url):
        """Tests that we gracefully handle User integrity violations"""
        dev_user_ = User.objects.create(
            email="testdev@ucl.ac.uk",
            cn="test",
            given_name="Test Dev",
            employee_id='testdev01'
        )
        app_ = App.objects.create(
            user=dev_user_,
            name="An App",
            callback_url="www.somecallbackurl.com/callback"
        )
        test_user = User.objects.create(
            email="testuser@ucl.ac.uk",
            cn="cn",
            given_name="Test Dev",
            employee_id='testuser01'
        )

        signer = signing.TimestampSigner()
        # Generate a random state for testing
        state = ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )
        data = app_.client_id + state
        signed_data = signer.sign(data)

        # Creation of new user should fail as cn has to be unique!
        # The "with" hack is needed when purposefully causing DB integrity
        # violations. @see: https://stackoverflow.com/a/23326971
        with transaction.atomic():
            user_data = {
                'userPrincipalName': 'eppn',
                'mailNickname': test_user.cn,
                'employeeId': 'newUser',
            }
            k = unittest.mock.patch('requests.post', side_effect=mocked_adcallback_post)
            k2 = unittest.mock.patch('requests.get', side_effect=lambda *args, **kwargs: mocked_ad_graph_get(*args, *kwargs, user_data=user_data, group_data=[]))
            k.start()
            k2.start()
            response = self.client.get(
                url,
                {
                    'appdata': signed_data
                },
            )
            self.assertEqual(response.status_code, 400)
            k.stop()
            k2.stop()

        # This update should fail as cn should be unique
        with transaction.atomic():
            user_data = {
                'userPrincipalName': 'eppn',
                'mailNickname': dev_user_.cn,
                'employeeId': test_user.employee_id,
            }
            k = unittest.mock.patch('requests.post', side_effect=mocked_adcallback_post)
            k2 = unittest.mock.patch('requests.get', side_effect=lambda *args, **kwargs: mocked_ad_graph_get(*args, *kwargs, user_data=user_data, group_data=[]))
            k.start()
            k2.start()
            response = self.client.get(
                url,
                {
                    'appdata': signed_data
                },
            )
            self.assertEqual(response.status_code, 400)
            k.stop()
            k2.stop()


    @parameterized.expand([
        ('/oauth/adcallback', 200, True),
        ('/dashboard/user/login.callback', 302, False),
        ('/settings/user/login.callback', 302, False)
    ])
    def test_valid_adcallback_real_account(self, url, expected_code, initial_data_exists):
        dev_user_ = User.objects.create(
            email="testdev@ucl.ac.uk",
            cn="test",
            given_name="Test Dev",
            employee_id='testdev01'
        )
        app_ = App.objects.create(
            user=dev_user_,
            name="An App",
            callback_url="www.somecallbackurl.com/callback"
        )

        signer = signing.TimestampSigner()
        # Generate a random state for testing
        state = ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )
        data = app_.client_id + state
        signed_data = signer.sign(data)

        user_data = {
            'userPrincipalName': 'eppn',
            'mailNickname': 'cn',
            'department': 'department',
            'givenName': 'givenname',
            'displayName': 'displayname',
            'employeeId': 'xxxtest01',
            'mail': 'mail',
            'surname': 'sn',
            'user_types': 'U/G'
        }

        group_data = [{'mailNickname': 'uclintranetgroups'}]
        k = unittest.mock.patch('requests.post', side_effect=mocked_adcallback_post)
        k2 = unittest.mock.patch('requests.get', side_effect=lambda *args, **kwargs: mocked_ad_graph_get(*args, *kwargs, user_data=user_data, group_data=group_data))
        k.start()
        k2.start()
        response = self.client.get(
            url,
            {
                'state': signed_data
            },
        )
        k.stop()
        k2.stop()

        # Load the new test user from DB
        test_user_ = User.objects.get(employee_id=user_data['employeeId'])
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(self.client.session['user_id'], test_user_.id)
        # Test that all fields were filled in correctly.
        self.assertEqual(test_user_.email, user_data['userPrincipalName'])
        self.assertEqual(test_user_.cn, user_data['mailNickname'])
        self.assertEqual(test_user_.employee_id, user_data['employeeId'])
        self.assertEqual(test_user_.raw_intranet_groups, "uclintranetgroups")
        self.assertEqual(test_user_.department, user_data['department'])
        self.assertEqual(test_user_.given_name, user_data['givenName'])
        self.assertEqual(test_user_.full_name, user_data['displayName'])
        self.assertEqual(test_user_.mail, user_data['mail'])
        self.assertEqual(test_user_.sn, user_data['surname'])
        self.assertEqual(test_user_.user_types, user_data['user_types'])

        # Now update all the values.
        user_data = {
            'userPrincipalName': 'testxxx@ucl.ac.uk',
            'mailNickname': 'testxxx',
            'department': 'Dept of Tests',
            'givenName': 'Test New Name',
            'displayName': 'Test User',
            'employeeId': 'xxxtest01',
            'mail': 'test.name.01@ucl.ac.uk',
            'surname': 'Second Name',
            'user_types': 'P/G',
        }
        group_data = [{'mailNickname': 'ucl-all'}, {'onPremisesSamAccountName': 'ucl-tests-all'}]
        k = unittest.mock.patch('requests.post', side_effect=mocked_adcallback_post)
        k2 = unittest.mock.patch('requests.get', side_effect=lambda *args, **kwargs: mocked_ad_graph_get(*args, *kwargs, user_data=user_data, group_data=group_data))
        k.start()
        k2.start()
        response = self.client.get(
            url,
            {
                'state': signed_data
            },
        )
        k.stop()
        k2.stop()

        # Reload the test user from DB
        test_user_ = User.objects.get(id=test_user_.id)
        self.assertEqual(response.status_code, expected_code)
        self.assertEqual(self.client.session['user_id'], test_user_.id)
        # Test that all fields were updated correctly.
        self.assertEqual(test_user_.email, user_data['userPrincipalName'])
        self.assertEqual(test_user_.cn, user_data['mailNickname'])
        self.assertEqual(test_user_.employee_id, user_data['employeeId'])
        self.assertEqual(test_user_.raw_intranet_groups, "ucl-all;ucl-tests-all")
        self.assertEqual(test_user_.department, user_data['department'])
        self.assertEqual(test_user_.given_name, user_data['givenName'])
        self.assertEqual(test_user_.full_name, user_data['displayName'])
        self.assertEqual(test_user_.mail, user_data['mail'])
        self.assertEqual(test_user_.sn, user_data['surname'])
        self.assertEqual(test_user_.user_types, user_data['user_types'])

        if initial_data_exists:
            initial_data = json.loads(response.context['initial_data'])
            self.assertEqual(
                initial_data['app_name'],
                app_.name
            )
            self.assertEqual(
                initial_data['client_id'],
                app_.client_id
            )
            self.assertEqual(
                initial_data['state'],
                state
            )
            self.assertDictEqual(
                initial_data['user'],
                {
                    "full_name": user_data['displayName'],
                    "cn": user_data['mailNickname'],
                    "email": user_data['userPrincipalName'],
                    "department": user_data['department'],
                    "upi": user_data['employeeId']
                }
            )

    def test_auto_accept_adcallback_real_account(self):
        dev_user_ = User.objects.create(
            email="testdev@ucl.ac.uk",
            cn="test",
            given_name="Test Dev",
            employee_id='testdev01'
        )
        app_ = App.objects.create(
            user=dev_user_,
            name="An App",
            callback_url="www.somecallbackurl.com/callback"
        )
        test_user_ = User.objects.create(
            email="testxxx@ucl.ac.uk",
            cn="testxxx",
            given_name="Test User",
            employee_id='xxxtest01'
        )

        signer = signing.TimestampSigner()
        # Generate a random state for testing
        state = ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )
        data = app_.client_id + state
        signed_data = signer.sign(data)

        app_scope = app_.scope
        app_scope.id = None
        app_scope.save()

        # Now set up a new token with that scope
        token = OAuthToken(
            app=app_,
            user=test_user_,
            scope=app_scope
        )
        token.save()

        user_data = {
            'userPrincipalName': 'testxxx@ucl.ac.uk',
            'mailNickname': 'testxxx',
            'department': 'Dept of Tests',
            'givenName': 'Test New Name',
            'displayName': 'Test User',
            'employeeId': 'xxxtest01',
            'mail': 'test.name.01@ucl.ac.uk',
            'surname': 'Second Name',
        }
        group_data = [{'mailNickname': 'ucl-all'}, {'onPremisesSamAccountName': 'ucl-tests-all'}]
        k = unittest.mock.patch('requests.post', side_effect=mocked_adcallback_post)
        k2 = unittest.mock.patch('requests.get', side_effect=lambda *args, **kwargs: mocked_ad_graph_get(*args, *kwargs, user_data=user_data, group_data=group_data))
        k.start()
        k2.start()
        response = self.client.get(
            '/oauth/adcallback',
            {
                'state': signed_data
            },
        )
        k.stop()
        k2.stop()
        self.assertEqual(response.status_code, 302)

    def test_userallow_no_post_data(self):
        response = self.client.get(
            '/oauth/user/allow',
            {}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"],
                         ("The signed data received "
                          "was invalid."
                          " Please try the login process again."
                          " If this issue persists, please contact us at "
                          "isd.apiteam@ucl.ac.uk or on github."))

    def test_userallow_bad_but_signed_post_data(self):
        signer = signing.TimestampSigner()
        signed_data = signer.sign("")
        response = self.client.post(
            '/oauth/user/allow',
            {
                'signed_app_data': signed_data
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"],
                         ("The JSON data was not in the expected format. "
                          "Please contact us at "
                          "isd.apiteam@ucl.ac.uk or on github."))

    def test_userdeny_no_post_data(self):
        response = self.client.get(
            '/oauth/user/deny',
            {}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"],
                         ("The signed data received "
                          "was invalid."
                          " Please try the login process again."
                          " If this issue persists, please contact us at "
                          "isd.apiteam@ucl.ac.uk or on github."))

    def test_userdeny_bad_but_signed_post_data(self):
        signer = signing.TimestampSigner()
        signed_data = signer.sign("")
        response = self.client.post(
            '/oauth/user/deny',
            {
                'signed_app_data': signed_data
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"],
                         ("The JSON data was not in the expected format. "
                          "Please contact us at "
                          "isd.apiteam@ucl.ac.uk or on github."))

    def test_userdeny_user_does_not_exist(self):
        dev_user_ = User.objects.create(
            email="testdev@ucl.ac.uk",
            cn="test",
            given_name="Test Dev",
            employee_id='testdev01'
        )
        app_ = App.objects.create(
            user=dev_user_,
            name="An App",
            callback_url="www.somecallbackurl.com/callback"
        )

        signer = signing.TimestampSigner()
        # Generate a random state for testing
        state = ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )

        response_data = {
            "client_id": app_.client_id,
            "state": state,
            "user_upi": "bogus"
        }

        response_data_str = json.dumps(response_data, cls=DjangoJSONEncoder)
        signed_data = signer.sign(response_data_str)

        response = self.client.post(
            '/oauth/user/deny',
            {
                'signed_app_data': signed_data
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"],
                         ("User does not exist. This should never occur. "
                          "Please contact us at "
                          "isd.apiteam@ucl.ac.uk or on github."))

    def test_userdeny_good_flow(self):
        dev_user_ = User.objects.create(
            email="testdev@ucl.ac.uk",
            cn="test",
            given_name="Test Dev",
            employee_id='testdev01'
        )
        app_ = App.objects.create(
            user=dev_user_,
            name="An App",
            callback_url="www.somecallbackurl.com/callback"
        )
        test_user_ = User.objects.create(
            email="testxxx@ucl.ac.uk",
            cn="testxxx",
            given_name="Test User",
            employee_id='xxxtest01'
        )
        signer = signing.TimestampSigner()
        # Generate a random state for testing
        state = ''.join(
            random.choices(string.ascii_letters + string.digits, k=32)
        )

        response_data = {
            "client_id": app_.client_id,
            "state": state,
            "user_upi": test_user_.employee_id
        }

        response_data_str = json.dumps(response_data, cls=DjangoJSONEncoder)
        signed_data = signer.sign(response_data_str)

        app_scope = app_.scope
        app_scope.id = None
        app_scope.save()

        token = OAuthToken(
            app=app_,
            user=test_user_,
            scope=app_scope
        )
        token.save()

        tokens = OAuthToken.objects.filter(app=app_, user=test_user_)
        for token in tokens:
            self.assertTrue(token.active)

        response = self.client.post(
            '/oauth/user/deny',
            {
                'signed_app_data': signed_data
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         app_.callback_url + "?result=denied&state=" + state)
        tokens = OAuthToken.objects.filter(app=app_, user=test_user_)
        for token in tokens:
            self.assertFalse(token.active)


class AppHelpersTestCase(TestCase):
    def test_generate_random_verification_code(self):
        code = generate_random_verification_code()
        self.assertEqual(code[:6], "verify")
        self.assertEqual(len(code), 86)


class DeleteAToken(TestCase):
    def setUp(self):
        mock_status_code = unittest.mock.Mock()
        mock_status_code.status_code = 200

        self.factory = APIRequestFactory()

    def test_deauthorise_app(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create(
            scope_number=2
        )
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope
        )
        token_id = oauth_token.token
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': app_.client_secret,
                'client_id': app_.client_id
            }
        )
        request.session = {'user_id': user_.id}

        token_id = oauth_token.token
        deauthorise_app(request)
        with self.assertRaises(OAuthToken.DoesNotExist):
            oauth_token = OAuthToken.objects.get(token=token_id)

    def test_deauthorise_user_does_not_exist(self):
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'abcdefg',
                'client_id': '1234.1234'
            }
        )
        request.session = {'user_id': 999999999}
        with self.assertRaises(User.DoesNotExist):
            deauthorise_app(request)

    def test_deauthorise_no_client_id(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'abcdefg',
                'token': 'uclapi-123456'
            }
        )
        request.session = {'user_id': user_.id}

        response = deauthorise_app(request)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "A Client ID must be provided to deauthorise an app."
        )

    def test_deauthorise_bad_client_id(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': 'abcdefg',
                'token': 'uclapi-123456',
                'client_id': '404_not_found'
            }
        )
        request.session = {'user_id': user_.id}

        response = deauthorise_app(request)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "App does not exist with the Client ID provided."
        )

    def test_deauthorise_no_token_for_app_and_user(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        request = self.factory.get(
            '/oauth/testcase',
            {
                'client_secret': app_.client_secret,
                'client_id': app_.client_id
            }
        )

        request.session = {'user_id': user_.id}

        response = deauthorise_app(request)
        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content.decode())
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            (
                "The app with the Client ID provided does not have a "
                "token for this user, so no action was taken."
            )
        )


class OAuthUserDataTestCase(APITestCase):
    """Tests the /oauth/user/data endpoint"""
    fake_student = MockSet(
        MockModel(
            qtype2='UPI'
        )
    )
    studenta_objects = unittest.mock.patch(
        'timetable.models.StudentsA.objects',
        fake_student
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

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            cn="cn",
            department="Dept of UCL API",
            email="cryptic@ucl.ac.uk",
            full_name="First Last",
            given_name="First",
            employee_id="upi",
            raw_intranet_groups="group-all",
            sn="Last",
            mail="fname.lname.yr.20@ucl.ac.uk",
            user_types="U/G"
        )
        cls.dev = User.objects.create(email="test@ucl.ac.uk", cn="test", given_name="Test Test")
        cls.app = App.objects.create(user=cls.dev, name="An App")
        cls.oauth_scope = OAuthScope.objects.create()
        cls.oauth_token = OAuthToken.objects.create(app=cls.app, user=cls.user, scope=cls.oauth_scope)

    def setUp(self):
        self.expected_user_data = {
            "ok": True,
            "cn": "cn",
            "department": "Dept of UCL API",
            "email": "cryptic@ucl.ac.uk",
            "full_name": "First Last",
            "given_name": "First",
            "upi": "upi",
            "scope_number": 0,
            "ucl_groups": ["group-all"],
            "sn": "Last",
            "mail": "fname.lname.yr.20@ucl.ac.uk",
            "user_types": ["U/G"]
        }

    def test_userdata_non_student(self):
        """Tests that userdata is correctly returned for a non-student"""
        response = self.client.get(
            '/oauth/user/data', {'token': self.oauth_token.token, 'client_secret': self.app.client_secret})
        self.assertEqual(response.status_code, 200)
        self.expected_user_data['is_student'] = False
        self.assertJSONEqual(response.content.decode('utf-8'), self.expected_user_data)

    @studenta_objects
    @lock_objects
    def test_userdata_student(self):
        """Tests that userdata is correctly returned for a student"""
        response = self.client.get(
            '/oauth/user/data', {'token': self.oauth_token.token, 'client_secret': self.app.client_secret})
        self.assertEqual(response.status_code, 200)
        self.expected_user_data['is_student'] = True
        self.assertJSONEqual(response.content.decode('utf-8'), self.expected_user_data)
