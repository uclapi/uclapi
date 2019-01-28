import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from django.conf import settings
import redis

from .app_helpers import is_url_safe, generate_api_token, \
    generate_app_client_id, generate_app_client_secret, \
    generate_app_id, get_articles
from .middleware.fake_shibboleth_middleware import FakeShibbolethMiddleWare
from .models import App, User
from .webhook_views import (
    edit_webhook, refresh_verification_secret, user_owns_app, verify_ownership
)
from dashboard.api_applications import (
    create_app, delete_app, regenerate_app_token, rename_app, set_callback_url,
    update_scopes, get_user_by_id
)


class MediumArticleScraperTestCase(TestCase):
    def test_articles_retrieved(self):
        medium_article_iterator = [
            {'title': 'a', 'url': 'b'},
            {'title': 'c', 'url': 'd'},
            {'title': 'e', 'url': 'f'}
        ]
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        for i in range(0, len(medium_article_iterator)):
            article = medium_article_iterator[i]
            redis_key_url = "Blog:item:{}:url".format(i)
            redis_key_title = "Blog:item:{}:title".format(i)
            self._redis.set(redis_key_url, article['url'])
            self._redis.set(redis_key_title, article['title'])
        articles = get_articles()
        self.assertEqual(articles, medium_article_iterator)


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
        self.assertTrue(token.startswith("uclapi-"))
        self.assertEqual(len(token), 70)
        self.assertEqual(token[22], "-")
        self.assertEqual(token[38], "-")
        self.assertEqual(token[54], "-")

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
            "Make sure to follow the documentation: "
            "https://uclapi.com/docs#webhook/challenge-event"
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


class VerifyOwnershipTestCase(TestCase):
    def mocked_request_correct_challenge_behaviour(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return {
                    "challenge": self.json_data["challenge"]
                }

        return MockResponse(kwargs['json'], 200)

    def mocked_request_incorrect_challenge_behaviour(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return {
                    "challenge": self.json_data["challenge"] + "1"
                }

        return MockResponse(kwargs['json'], 200)

    @patch(
        "requests.post",
        side_effect=mocked_request_correct_challenge_behaviour
    )
    def test_verify_ownership_success(self, mock):
        self.assertTrue(
            verify_ownership("https://bestapp", "1234", "secret")
        )

    @patch(
        "requests.post",
        side_effect=mocked_request_incorrect_challenge_behaviour
    )
    def test_verify_ownership_failure(self, mock):
        self.assertFalse(
            verify_ownership("https://bestapp", "1234", "secret")
        )


class RefreshVerifcationSecretViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create(cn="test1", employee_id=1)
        self.app1 = App.objects.create(user=self.user1, name="An App")

        self.user2 = User.objects.create(cn="test2", employee_id=2)
        self.app2 = App.objects.create(user=self.user2, name="Another App")

    def test_refresh_verification_secret_GET(self):
        request = self.factory.get('/')
        response = refresh_verification_secret(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(content["message"], "Request is not of method POST")

    def test_refresh_verification_secret_POST_missing_parameters(self):
        request = self.factory.post('/')
        response = refresh_verification_secret(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["message"],
            "Request is missing parameters. Should have app_id"
            " as well as a sessionid cookie"
        )

    def test_refresh_verification_secret_POST_user_does_not_own_app(self):
        request = self.factory.post(
            '/',
            {
                'app_id': self.app2.id
            }
        )
        request.session = {'user_id': self.user1.id}
        response = refresh_verification_secret(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(content["ok"])
        self.assertEqual(
            content["message"],
            "App does not exist or user is lacking permission."
        )

    def test_refresh_verification_secret_POST_success(
        self
    ):

        request = self.factory.post(
            '/',
            {
                'app_id': self.app1.id
            }
        )
        request.session = {'user_id': self.user1.id}
        response = refresh_verification_secret(request)

        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content["ok"])
        self.assertTrue("new_secret" in content.keys())


def post_request_only(self, url, view):
    request = self.factory.get(
        url,
        {
        }
    )

    response = view(request)
    content = json.loads(response.content.decode())
    self.assertEqual(response.status_code, 400)
    self.assertEqual(
        content["error"],
        "Request is not of method POST"
    )


def empty_get_request_only(self, url, view, error):
    request = self.factory.post(
        url,
        {
        }
    )

    response = view(request)
    content = json.loads(response.content.decode())
    self.assertEqual(response.status_code, 400)
    self.assertEqual(
        content["message"],
        error
    )


class ApiApplicationsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # self.functions maps urls to a tuple cotaining a view
        # and a number relating to an error message from
        # errors

        self.functions = {
            '/api/create/': (create_app, 0), '/api/rename/': (rename_app, 1),
            '/api/regen/': (regenerate_app_token, 2),
            '/api/delete/': (delete_app, 2),
            '/api/setcallbackurl/': (set_callback_url, 2),
            '/api/updatescopes/': (update_scopes, 2)
        }
        self.errors = (
            "Request does not have name or user.",
            "Request does not have app_id/new_name",
            "Request does not have an app_id."
        )

    def test_get_user_returns_correct_user(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        self.assertEqual(get_user_by_id(user_.id), user_)

    def test_get_request_rejected(self):
        for url in self.functions:
            post_request_only(self, url, self.functions[url][0])

    def test_missing_parameters(self):
        for url in self.functions:
            empty_get_request_only(
                self,
                url,
                self.functions[url][0],
                self.errors[self.functions[url][1]]
            )

    # Start of create_app section

    def test_app_creation_success(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        request = self.factory.post(
            '/api/create/',
            {
                "name": "test_app"
            }
        )
        request.session = {'user_id': user_.id}
        response = create_app(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "App sucessfully created"
        )
        self.assertTrue(len(App.objects.filter(
            name="test_app",
            user=user_,
            deleted=False)) != 0)

    # Start of rename_app section

    def test_rename_not_existing_app(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        request = self.factory.post(
            '/api/rename/',
            {
                "new_name": "test_app",
                "app_id": 1
            }
        )
        request.session = {'user_id': user_.id}
        response = rename_app(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "App does not exist."
        )
