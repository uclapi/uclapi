import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory

from .app_helpers import is_url_safe, generate_api_token, \
    generate_app_client_id, generate_app_client_secret, \
    generate_app_id
from .middleware.fake_shibboleth_middleware import FakeShibbolethMiddleWare
from .models import App, User
from .webhook_views import edit_webhook, user_owns_app


class DashboardTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(email="test@test.com",
                                full_name="Test testington",
                                given_name="test",
                                department="CS",
                                cn="test",
                                raw_intranet_groups="none",
                                employee_id=12345
                                )
        App.objects.create(user=u,
                           name="An App")
        session = self.client.session
        session["user_id"] = u.id
        session.save()

    def test_id_not_set(self):
        with patch.dict(
            'os.environ',
            {'SHIBBOLETH_ROOT': "http://rooturl.com"}
        ):
            session = self.client.session
            session.pop("user_id")
            session.save()

            res = self.client.get('/dashboard/')
            self.assertRedirects(
                res,
                "http://rooturl.com/Login?target="
                "http%3A//testserver/dashboard/user/login.callback",
                fetch_redirect_response=False,
            )

    def test_get_agreement(self):
        res = self.client.get('/dashboard/')
        self.assertTemplateUsed(res, "agreement.html")

    def test_post_agreement(self):
        res = self.client.post('/dashboard/')
        self.assertTemplateUsed(res, "agreement.html")
        self.assertContains(res, "You must agree to the fair use policy")

        res = self.client.post('/dashboard/', {'agreement': 'some rubbish'})
        self.assertTemplateUsed(res, "agreement.html")
        self.assertContains(res, "You must agree to the fair use policy")

        res = self.client.post('/dashboard/', {'agreement': 'True'})
        self.assertTemplateUsed(res, "dashboard.html")
        self.assertContains(res, "An App")
        self.assertContains(res, "Test testington")

    def test_unsafe_urls(self):
        assert not is_url_safe("ftp://test.com")
        assert not is_url_safe("https://uclapi.com/callback")
        assert not is_url_safe("ssh://uclapi.com/callback")

    def test_safe_url(self):
        assert is_url_safe("https://mytestapp.com/callback")
        assert is_url_safe("https://uclapiexample.com/callback")


class FakeShibbolethMiddleWareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = FakeShibbolethMiddleWare()

    def test_process_request_GET_with_header(self):
        request = self.factory.get(
            '/',
            {"convert-get-headers": "1", "key1": "value1", "key2": "value2"}
        )
        self.middleware.process_request(request)

        self.assertEqual(request.META.get("HTTP_CONVERT-GET-HEADERS"), "1")
        self.assertEqual(request.META.get("HTTP_KEY1"), "value1")
        self.assertEqual(request.META.get("HTTP_KEY2"), "value2")

    def test_process_request_GET_without_header(self):
        request = self.factory.get(
            '/',
            {"key1": "value1", "key2": "value2"}
        )
        self.middleware.process_request(request)

        self.assertIsNone(request.META.get("key1"))
        self.assertIsNone(request.META.get("key2"))

    def test_process_request_POST_with_header(self):
        request = self.factory.post(
            '/',
            {"convert-post-headers": "1", "key1": "value1", "key2": "value2"}
        )
        self.middleware.process_request(request)

        self.assertEqual(request.META.get("key1"), "value1")
        self.assertEqual(request.META.get("key2"), "value2")

    def test_process_request_POST_without_header(self):
        request = self.factory.post(
            '/',
            {"key1": "value1", "key2": "value2"}
        )

        self.assertIsNone(request.META.get("key1"))
        self.assertIsNone(request.META.get("key2"))


class DashboardAppHelpersTestCase(TestCase):
    def test_generate_api_token(self):
        token = generate_api_token()
        self.assertEqual(token[:6], "uclapi")
        self.assertEqual(len(token), 66)
        self.assertEqual(token[6], "-")
        self.assertEqual(token[21], "-")
        self.assertEqual(token[36], "-")
        self.assertEqual(token[51], "-")

    def test_generate_app_client_id(self):
        client_id = generate_app_client_id()
        self.assertEqual(client_id[16], '.')
        self.assertEqual(len(client_id), 33)

    def test_generate_app_client_secret(self):
        client_secret = generate_app_client_secret()
        self.assertEqual(len(client_secret), 64)

    def generate_app_id(self):
        app_id = generate_app_id()
        self.assertEqual(app_id[0], 'A')
        self.assertEqual(len(app_id), 11)


class URLSafetyTestCase(TestCase):
    def test_is_url_safe_full_success(self):
        self.assertTrue(
            is_url_safe("https://example.com")
        )

    def test_is_url_safe_https_failure(self):
        self.assertFalse(
            is_url_safe("http://example.com")
        )

    def test_is_url_safe_validators_failure(self):
        self.assertFalse(
            is_url_safe("https://asdasd.asd.asd.asd.1234")
        )

    def test_is_url_safe_validators_failure_private(self):
        self.assertFalse(
            is_url_safe("https://127.0.0.1")
        )

    def test_is_url_safe_validators_failure_private2(self):
        self.assertFalse(
            is_url_safe("https://10.0.0.1")
        )

    def test_is_url_safe_forbidden(self):
        self.assertFalse(
            is_url_safe("https://uclapi.com/test/test")
        )

    def test_is_url_safe_forbidden2(self):
        self.assertFalse(
            is_url_safe("https://staging.ninja/test/test")
        )
    # Testcase for whitelisted URL needed


class UserOwnsAppTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email="test@test.com",
            full_name="Test testington",
            given_name="test",
            department="CS",
            cn="test",
            raw_intranet_groups="none",
            employee_id=0
        )
        self.user2 = User.objects.create(
            email="test@testing.com",
            full_name="Test Er",
            given_name="Test",
            department="CS",
            cn="tester",
            raw_intranet_groups="none",
            employee_id=1
        )
        self.app1 = App.objects.create(
            user=self.user1,
            name="An App"
        )
        self.app2 = App.objects.create(user=self.user2, name="Another App")

    def test_user_owns_nonexistent_app(self):
        self.assertFalse(user_owns_app(self.user1.id, 123))

    def test_user_owns_app_belonging_to_other_user(self):
        self.assertFalse(user_owns_app(self.user1.id, self.app2.id))

    def test_user_owns_app_belonging_to_him(self):
        self.assertTrue(user_owns_app(self.user1.id, self.app1.id))


class WebHookRequestViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create(cn="test1", employee_id=1)
        self.app1 = App.objects.create(user=self.user1, name="An App")

        self.user2 = User.objects.create(cn="test2", employee_id=2)
        self.app2 = App.objects.create(user=self.user2, name="Another App")

    def test_edit_webhook_GET(self):
        request = self.factory.get('/')
        response = edit_webhook(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["message"], "Request is not of method POST")

    def test_edit_webhook_POST_missing_parameters(self):
        request = self.factory.post('/')
        response = edit_webhook(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["message"],
            "Request is missing parameters. Should have app_id"
            ", url, siteid, roomid, contact"
            " as well as a sessionid cookie"
        )

    def test_edit_webhook_POST_user_does_not_own_app(self):
        request = self.factory.post(
            '/',
            {
                'app_id': self.app2.id, 'siteid': 1, 'roomid': 1,
                'contact': 1, 'url': 1
            }
        )
        request.session = {'user_id': self.user1.id}
        response = edit_webhook(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["message"],
            "App does not exist or user is lacking permission."
        )

    @patch("dashboard.webhook_views.verify_ownership", lambda *args: False)
    @patch("dashboard.webhook_views.is_url_safe", lambda *args: True)
    def test_edit_webhook_POST_ownership_verification_fail(
        self
    ):

        request = self.factory.post(
            '/',
            {
                'app_id': self.app1.id, 'siteid': 2, 'roomid': 2,
                'contact': 2, 'url': "http://new"
            }
        )
        request.session = {'user_id': self.user1.id}
        response = edit_webhook(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["message"],
            "Ownership of webhook can't be verified."
            "[Link to relevant docs here]"
        )

    @patch("dashboard.webhook_views.verify_ownership", lambda *args: True)
    @patch("dashboard.webhook_views.is_url_safe", lambda *args: True)
    @patch("keen.add_event", lambda *args: None)
    def test_edit_webhook_POST_user_owns_app_changing_url_verification_ok(
        self
    ):

        request = self.factory.post(
            '/',
            {
                'app_id': self.app1.id, 'siteid': 2, 'roomid': 2,
                'contact': 2, 'url': "http://new"
            }
        )
        request.session = {'user_id': self.user1.id}
        response = edit_webhook(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content["ok"])
        self.assertEqual(content["message"], "Webhook sucessfully changed.")
