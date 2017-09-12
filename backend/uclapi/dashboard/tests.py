from unittest.mock import patch

from django.test import RequestFactory, TestCase

from .app_helpers import is_url_safe,generate_api_token, \
    generate_app_client_id, generate_app_client_secret, \
    generate_app_id
from .middleware.fake_shibboleth_middleware import FakeShibbolethMiddleWare
from .models import App, User


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
