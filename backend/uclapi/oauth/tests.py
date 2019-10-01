import json
import os
import random
import string
import unittest.mock

from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory
from django.core import signing

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse

from dashboard.models import App, User

from .app_helpers import generate_random_verification_code
from .models import OAuthScope, OAuthToken
from .scoping import Scopes
from .views import authorise, shibcallback, deauthorise_app


@uclapi_protected_endpoint(personal_data=True, required_scopes=["timetable"])
def test_timetable_request(request, *args, **kwargs):
    return JsonResponse({
        "ok": True
    }, custom_header_data=kwargs)


def unsign(data, max_age):
    raise signing.SignatureExpired


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
            {'SHIBBOLETH_ROOT': 'FakeShibDirectory'}
        )
        k.start()
        response = authorise(request)
        k.stop()
        self.assertEqual(response.status_code, 302)

    def test_no_signed_data(self):
        request = self.factory.get(
            '/oauth/shibcallback',
            {
            }
        )
        response = shibcallback(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            "No signed app data returned from Shibboleth."
            " Please use the authorise endpoint."
        )

    def test_invalid_signed_data(self):
        request = self.factory.get(
            '/oauth/shibcallback',
            {
                'appdata': "invalid"
            }
        )
        response = shibcallback(request)
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
            '/oauth/shibcallback',
            {
                'appdata': "invalid"
            }
        )
        response = shibcallback(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["error"],
            ("Login data has expired. Please attempt to log in again. "
             "If the issues persist please contact the UCL API "
             "Team to rectify this.")
        )

    def test_valid_shibcallback_real_account(self):
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

        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            HTTP_EPPN='testxxx@ucl.ac.uk',
            HTTP_CN='testxxx',
            HTTP_DEPARTMENT='Dept of Tests',
            HTTP_GIVENNAME='Test New Name',
            HTTP_DISPLAYNAME='Test User',
            HTTP_EMPLOYEEID='xxxtest01',
            HTTP_UCLINTRANETGROUPS='ucl-all;ucl-tests-all'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['user_id'], test_user_.id)

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
                "full_name": "Test User",
                "cn": "testxxx",
                "email": "testxxx@ucl.ac.uk",
                "department": "Dept of Tests",
                "upi": "xxxtest01"
            }
        )

        # Reload the test user from DB
        test_user_ = User.objects.get(id=test_user_.id)

        self.assertEqual(
            test_user_.given_name,
            "Test New Name"
        )

        # Now lets test for when UCL doesn't give us department the department,
        # givenname and displayname.
        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            HTTP_EPPN='testxxx@ucl.ac.uk',
            HTTP_CN='testxxx',
            # NOTE: missing HTTP_DEPARTMENT, HTTP_GIVENNAME, HTTP_DISPLAYNAME
            HTTP_EMPLOYEEID='xxxtest01',
            HTTP_UCLINTRANETGROUPS='ucl-all;ucl-tests-all'
        )
        self.assertEqual(response.status_code, 200)

        # Reload the test user from DB
        test_user_ = User.objects.get(id=test_user_.id)

        # If a non-critical HTTP header is not passed, we don't want to
        # overwrite the previous value with an empty string.
        self.assertEqual(
            test_user_.department,
            "Dept of Tests"
        )
        self.assertEqual(
            test_user_.given_name,
            "Test New Name"
        )
        self.assertEqual(
            test_user_.full_name,
            "Test User"
        )

        # Now let's test when critical fields are missing
        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            # NOTE: missing critical field eppn
            HTTP_CN='testxxx',
            HTTP_EMPLOYEEID='xxxtest01',
            HTTP_DEPARTMENT='Dept of Tests',
            HTTP_GIVENNAME='Test New Name',
            HTTP_DISPLAYNAME='Test User',
            HTTP_UCLINTRANETGROUPS='ucl-all;ucl-tests-all'
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            HTTP_EPPN='testxxx@ucl.ac.uk',
            # NOTE: missing critical field cn
            HTTP_DEPARTMENT='Dept of Tests',
            HTTP_GIVENNAME='Test New Name',
            HTTP_DISPLAYNAME='Test User',
            HTTP_EMPLOYEEID='xxxtest01',
            HTTP_UCLINTRANETGROUPS='ucl-all;ucl-tests-all'
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            HTTP_EPPN='testxxx@ucl.ac.uk',
            HTTP_CN='testxxx',
            # NOTE: missing critical field employee_id (aka UPI)
            HTTP_DEPARTMENT='Dept of Tests',
            HTTP_GIVENNAME='Test New Name',
            HTTP_DISPLAYNAME='Test User',
            HTTP_UCLINTRANETGROUPS='ucl-all;ucl-tests-all'
        )
        self.assertEqual(response.status_code, 400)


    def test_valid_shibcallback_test_account(self):
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

        response = self.client.get(
            '/oauth/shibcallback',
            {
                'appdata': signed_data
            },
            HTTP_EPPN='testxxx@ucl.ac.uk',
            HTTP_CN='testxxx',
            HTTP_DEPARTMENT='Shibtests',
            HTTP_GIVENNAME='Test',
            HTTP_DISPLAYNAME='Test User',
            HTTP_EMPLOYEEID='xxxtest01',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['user_id'], test_user_.id)

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
                "full_name": "Test User",
                "cn": "testxxx",
                "email": "testxxx@ucl.ac.uk",
                "department": "Shibtests",
                "upi": "xxxtest01"
            }
        )

        # Reload the test user from DB
        test_user_ = User.objects.get(id=test_user_.id)

        self.assertEqual(
            test_user_.raw_intranet_groups,
            "shibtests"
        )


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
