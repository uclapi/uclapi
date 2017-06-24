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

        self.assertEqual(equal, True)

    def test_check_scope(self):
        self.assertEqual(self.s.check_scope(12, "roombookings"), False)
        self.assertEqual(self.s.check_scope(12, "uclu"), True)

    def test_get_all_scopes(self):
        scopes_bare = self.s.get_all_scopes(pretty_print=False)
        self.assertEqual({
            "name": "roombookings",
            "id": 0
        } in scopes_bare, True)

        scopes_pretty = self.s.get_all_scopes(pretty_print=True)
        self.assertEqual({
            "name": "roombookings",
            "description": "Private room bookings data"
        } in scopes_pretty, True)

    def test_scopes_dict(self):
        scopes_dict = self.s.scope_dict(5, pretty_print=False)
        self.assertEqual(scopes_dict, [
            {
                "name": "roombookings",
                "id": 0
            },
            {
                "name": "uclu",
                "id": 2
            }
        ])


class OAuthTokenCheckDecoratorTestCase(TestCase):
    def setUp(self):
        mock_status_code = unittest.mock.Mock()
        mock_status_code.status_code = 200
        mock_view_func = unittest.mock.Mock(return_value=mock_status_code)

        self.dec_view = oauth_token_check(required_scopes=[])(mock_view_func)
        self.factory = APIRequestFactory()

    def test_decorator_no_client_secret_proof_provided(self):
        request = self.factory.get('/')
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No Client Secret Proof provided")

    def test_decorator_no_token_provided(self):
        request = self.factory.get(
            '/',
            {'client_secret_proof': 'not_a_real_proof'}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "No token provided via GET.")

    def test_decorator_nonexistent_token_provided(self):
        request = self.factory.get(
            '/',
            {'client_secret_proof': 'not_a_real_secret_proof', 'token': 'fake'}
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["error"], "Token does not exist")

    def test_decorator_client_secret_verification_failed(self):
        # create User, App, and OAuth it
        user_ = User.objects.create(
            email="test@ucl.ac.uk", cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create()
        oauth_token = OAuthToken.objects.create(
            app=app_, user=user_, scope=oauth_scope
        )

        request = self.factory.get(
            '/',
            {
                'client_secret_proof': 'not_a_real_proof',
                'token': oauth_token.token
            }
        )
        response = self.dec_view(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["error"],
            "Client secret HMAC verification failed."
        )

    def test_decorator_no_permission_to_access(self):
        pass

    def test_decorator_everything_passes(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk", cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        oauth_scope = OAuthScope.objects.create()
        oauth_token = OAuthToken.objects.create(
            app=app_, user=user_, scope=oauth_scope
        )

        # TODO: THIS WILL GET CHANGED
        # calculate the client_secret_proof
        import hmac, hashlib, base64
        hmac_digest = hmac.new(
            bytes(app_.client_secret, 'ascii'),
            msg=oauth_token.token.encode('ascii'),
            digestmod=hashlib.sha256
        ).digest()
        hmac_b64 = base64.b64encode(hmac_digest).decode()

        request = self.factory.get(
            '/',
            {'client_secret_proof': hmac_b64, 'token': oauth_token.token}
        )
        response = self.dec_view(request)

        self.assertEqual(response.status_code, 200)
