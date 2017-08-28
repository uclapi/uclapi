import json
import unittest.mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from dashboard.models import App, User

from .decorators import oauth_token_check
from .models import OAuthScope, OAuthToken
from .scoping import Scopes


class ScopingTestCase(TestCase):
    def setUp(self):
        self.s = Scopes()
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

    def test_remove_scope(self):
        self.scope_a.scope_number = 3
        self.scope_a.scope_number = self.s.remove_scope(
                                        self.scope_a.scope_number,
                                        "roombookings"
                                    )
        self.scope_a.save()

        self.assertEqual(self.scope_a.scope_number, 2)

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


class OAuthTokenCheckDecoratorTestCase(TestCase):
    def setUp(self):
        mock_status_code = unittest.mock.Mock()
        mock_status_code.status_code = 200
        self.mock_view_func = unittest.mock.Mock(return_value=mock_status_code)

        self.dec_view = oauth_token_check(
            required_scopes=[]
        )(self.mock_view_func)

        self.factory = APIRequestFactory()

    def test_decorator_no_client_secret_provided(self):
        request = self.factory.get('/')
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No Client Secret provided.")

    def test_decorator_no_token_provided(self):
        request = self.factory.get(
            '/',
            {'client_secret': 'not_a_real_secret'}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No token provided via GET.")

    def test_decorator_nonexistent_token_provided(self):

        request = self.factory.get(
            '/',
            {
                'client_secret': 'not_a_real_secret',
                'token': 'fake'
            }
        )
        response = self.dec_view(request)

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
            '/',
            {
                'client_secret': 'not_a_real_secret',
                'token': oauth_token.token
            }
        )
        response = self.dec_view(request)

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
            scope_number=1,
        )
        app_ = App.objects.create(
            user=user_,
            name="An App",
            scope=oauth_scope_app
        )
        oauth_scope_user = OAuthScope.objects.create(
            scope_number=2
        )
        oauth_token = OAuthToken.objects.create(
            app=app_,
            user=user_,
            scope=oauth_scope_user
        )

        request = self.factory.get(
            '/',
            {
                'token': oauth_token.token,
                'client_secret': app_.client_secret
            }
        )

        dec_view_rb = oauth_token_check(
            required_scopes=["roombookings"]
        )(self.mock_view_func)

        response = dec_view_rb(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "The token provided does not have permission"
            " to access this data."
        )

    def test_decorator_everything_passes(self):
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
            '/',
            {
                'client_secret': app_.client_secret,
                'token': oauth_token.token
            }
        )
        response = self.dec_view(request)

        self.assertEqual(response.status_code, 200)
