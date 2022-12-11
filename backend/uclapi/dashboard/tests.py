import json
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.utils.datetime_safe import datetime
from rest_framework.test import APIRequestFactory
from django.conf import settings
import redis

from common.decorators import throttle_api_call
from oauth.models import OAuthToken, OAuthScope
from uclapi.settings import REDIS_UCLAPI_HOST
from .app_helpers import is_url_unsafe, generate_api_token, \
    generate_app_client_id, generate_app_client_secret, \
    generate_app_id, get_articles
from .models import App, User, APICall
from .webhook_views import (
    edit_webhook, refresh_verification_secret, user_owns_app, verify_ownership
)
from dashboard.api_applications import (
    create_app, delete_app, regenerate_app_token, rename_app, set_callback_url,
    update_scopes, get_user_by_id, number_of_requests, quota_remaining,
    users_per_app, users_per_app_by_dept, most_popular_service,
    most_popular_method
)


class MediumArticleScraperTestCase(TestCase):
    def test_articles_retrieved(self):
        medium_article_iterator = [
            {'title': 'a',
                'url': 'b',
                'tags': 'c',
                'creator': 'd',
                'published': 'e',
                'updated': 'e',
                'content': 'f',
                'image_url': 'g',
             },
            {'title': 'h',
                'url': 'i',
                'tags': 'j',
                'creator': 'k',
                'published': 'l',
                'updated': 'm',
                'content': 'n',
                'image_url': 'o',
             },
            {'title': 'p',
                'url': 'q',
                'tags': 'r',
                'creator': 's',
                'published': 't',
                'updated': 'u',
                'content': 'v',
                'image_url': 'w',
             },
        ]
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        pipe = self._redis.pipeline()
        for i in range(0, len(medium_article_iterator)):
            article = medium_article_iterator[i]
            redis_key_title = "Blog:item:{}:title".format(i)
            redis_key_url = "Blog:item:{}:url".format(i)
            redis_key_tags = "Blog:item:{}:tags".format(i)
            redis_key_creator = "Blog:item:{}:creator".format(i)
            redis_key_published = "Blog:item:{}:published".format(i)
            redis_key_updated = "Blog:item:{}:updated".format(i)
            redis_key_content = "Blog:item:{}:content".format(i)
            redis_key_image_url = "Blog:item:{}:image_url".format(i)
            pipe.set(redis_key_title, article['title'])
            pipe.set(redis_key_url, article['url'])
            pipe.set(redis_key_tags, article['tags'])
            pipe.set(redis_key_creator, article['creator'])
            pipe.set(redis_key_published, article['published'])
            pipe.set(redis_key_updated, article['updated'])
            pipe.set(redis_key_content, article['content'])
            pipe.set(redis_key_image_url, article['image_url'])
        pipe.execute()
        articles = get_articles()
        for i in range(0, len(medium_article_iterator)):
            redis_key_title = "Blog:item:{}:title".format(i)
            redis_key_url = "Blog:item:{}:url".format(i)
            redis_key_tags = "Blog:item:{}:tags".format(i)
            redis_key_creator = "Blog:item:{}:creator".format(i)
            redis_key_published = "Blog:item:{}:published".format(i)
            redis_key_updated = "Blog:item:{}:updated".format(i)
            redis_key_content = "Blog:item:{}:content".format(i)
            redis_key_image_url = "Blog:item:{}:image_url".format(i)
            pipe.delete(redis_key_url)
            pipe.delete(redis_key_title)
            pipe.delete(redis_key_tags)
            pipe.delete(redis_key_creator)
            pipe.delete(redis_key_published)
            pipe.delete(redis_key_updated)
            pipe.delete(redis_key_content)
            pipe.delete(redis_key_image_url)
        pipe.execute()
        self.assertEqual(articles, medium_article_iterator)


class DashboardTestCase(TestCase):

    TEST_USER = dict(
        email="test@test.com",
        full_name="Test testington",
        given_name="test",
        department="CS",
        cn="test",
        raw_intranet_groups="none",
        employee_id=12345
    )

    TEST_APP = dict(name="An App")

    def setUp(self):
        u = User.objects.create(**DashboardTestCase.TEST_USER)
        App.objects.create(user=u,
                           **DashboardTestCase.TEST_APP)
        session = self.client.session
        session["user_id"] = u.id
        session.save()

    def test_id_not_set(self):
        with patch.dict(
            'os.environ', {
                "AZURE_AD_ROOT": "http://rooturl.com",
                "AZURE_AD_CLIENT_ID": "foo",
                "UCLAPI_DOMAIN": "http://testserver"
            }
        ):
            session = self.client.session
            session.pop("user_id")
            session.save()

            res = self.client.get('/dashboard/')
            self.assertRedirects(
                res,
                "http://rooturl.com/oauth2/v2.0/authorize?client_id="
                "foo&response_type=code&scope=openid%20email%20profile%20user.read&response_mode=query&redirect_uri=http%3A//testserver/dashboard/user/login.callback",
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

    def test_unsafe_urls(self):
        assert is_url_unsafe("ftp://test.com")
        assert is_url_unsafe("https://uclapi.com/callback")
        assert is_url_unsafe("ssh://uclapi.com/callback")

    def test_safe_url(self):
        assert not is_url_unsafe("https://mytestapp.com/callback")
        assert not is_url_unsafe("https://uclapiexample.com/callback")

    def test_get_apps(self):
        session = self.client.session
        session.save()

        res = self.client.get('/dashboard/api/apps/')
        self.assertEqual(res.status_code, 200)

        content = json.loads(res.content.decode())
        self.assertEqual(
            content["name"],
            DashboardTestCase.TEST_USER["full_name"]
        )
        self.assertEqual(
            content["cn"],
            DashboardTestCase.TEST_USER["cn"]
        )
        self.assertEqual(
            content["department"],
            DashboardTestCase.TEST_USER["department"]
        )
        self.assertEqual(
            content["intranet_groups"],
            DashboardTestCase.TEST_USER["raw_intranet_groups"]
        )
        self.assertTrue(isinstance(content["apps"], list))
        self.assertEqual(len(content["apps"]), 1)
        self.assertEqual(
            content["apps"][0]["name"],
            DashboardTestCase.TEST_APP["name"]
        )


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

    def test_generate_app_id(self):
        app_id = generate_app_id()
        self.assertEqual(app_id[0], 'A')
        self.assertEqual(len(app_id), 11)


class URLSafetyTestCase(TestCase):
    def test_is_url_safe_full_success(self):
        self.assertFalse(
            is_url_unsafe("https://example.com")
        )

    def test_is_url_safe_https_failure(self):
        self.assertTrue(
            is_url_unsafe("http://example.com")
        )

    def test_is_url_safe_validators_failure(self):
        self.assertTrue(
            is_url_unsafe("https://asdasd.asd.asd.asd.1234")
        )

    def test_is_url_safe_validators_failure_private(self):
        self.assertTrue(
            is_url_unsafe("https://127.0.0.1")
        )

    def test_is_url_safe_validators_failure_private2(self):
        self.assertTrue(
            is_url_unsafe("https://10.0.0.1")
        )

    def test_is_url_safe_forbidden(self):
        self.assertTrue(
            is_url_unsafe("https://uclapi.com/test/test")
        )

    def test_is_url_safe_forbidden2(self):
        self.assertTrue(
            is_url_unsafe("https://staging.ninja/test/test")
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
    @patch("dashboard.webhook_views.is_url_unsafe", lambda *args: False)
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


def empty_post_request_only(self, url, view, error):
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


def no_app_post_request(self, url, view, user_):

    request = self.factory.post(
        url,
        {
            "new_name": "test_app",
            "app_id": 1
        }
    )
    request.session = {'user_id': user_.id}
    response = view(request)
    content = json.loads(response.content.decode())
    self.assertEqual(response.status_code, 400)
    self.assertEqual(
        content["message"],
        "App does not exist."
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
        self.r = redis.Redis(host=REDIS_UCLAPI_HOST)

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
            empty_post_request_only(
                self,
                url,
                self.functions[url][0],
                self.errors[self.functions[url][1]]
            )

    def test_app_does_not_exist(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        allowed_urls = ['/api/rename/', '/api/delete/', '/api/regen/']
        for url in self.functions:
            if url in allowed_urls:
                no_app_post_request(self, url, self.functions[url][0], user_)

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

    def test_rename_success_app(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/rename/',
            {
                "new_name": "test_app",
                "app_id": app_.id
            }
        )
        request.session = {'user_id': user_.id}
        self.assertTrue(len(App.objects.filter(
            name="test_app",
            user=user_,
            deleted=False)) == 0)
        self.assertTrue(len(App.objects.filter(
            name="An App",
            user=user_,
            deleted=False)) != 0)
        response = rename_app(request)
        self.assertTrue(len(App.objects.filter(
            name="test_app",
            user=user_,
            deleted=False)) != 0)
        self.assertTrue(len(App.objects.filter(
            name="An App",
            user=user_,
            deleted=False)) == 0)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "App sucessfully renamed."
        )

    def test_delete_app_success(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/delete/',
            {
                "app_id": app_.id
            }
        )
        request.session = {'user_id': user_.id}
        self.assertTrue(len(App.objects.filter(
            name="An App",
            user=user_,
            deleted=False)) != 0)
        response = delete_app(request)
        self.assertTrue(len(App.objects.filter(
            name="An App",
            user=user_,
            deleted=False)) == 0)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "App sucessfully deleted."
        )

    def test_regen_token_success(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/regen/',
            {
                "app_id": app_.id
            }
        )
        request.session = {'user_id': user_.id}
        response = regenerate_app_token(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "App token sucessfully regenerated."
        )
        self.assertEqual(
            content["app"]["id"],
            app_.id
        )
        self.assertTrue(
            content["app"]["token"] != app_.api_token
        )

    def test_change_callback_not_in_session(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": app_.id,
            }
        )
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "User ID not set in session. Please log in again."
        )

    def test_change_callback_no_url_provided(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": app_.id,
            }
        )
        request.session = {'user_id': user_.id}
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "Request does not have a Callback URL."
        )

    def test_change_callback_app_does_not_exist(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": 100000000000001,
                "callback_url": "https://testcall.com"
            }
        )
        request.session = {'user_id': user_.id}
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "App does not exist."
        )

    def test_change_callback_url_not_valid(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": app_.id,
                "callback_url": "NotReallyAURL"
            }
        )
        request.session = {'user_id': user_.id}
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], "The requested callback URL is not valid.")

    def test_change_callback_url_https_not_valid(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": app_.id,
                "callback_url": "https://a"
            }
        )
        request.session = {'user_id': user_.id}
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "The requested callback URL is not valid."
        )

    def test_change_callback_url_success(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/setcallbackurl/',
            {
                "app_id": app_.id,
                "callback_url": "https://testcall.com"
            }
        )
        request.session = {'user_id': user_.id}
        response = set_callback_url(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "Callback URL successfully changed."
        )
        app_ = App.objects.filter(id=app_.id, user=user_.id)[0]
        self.assertTrue(app_.callback_url == "https://testcall.com")

    def test_change_scopes_not_in_session(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": app_.id,
            }
        )
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "User ID not set in session. Please log in again."
        )

    def test_change_scopes_no_scope_data(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": app_.id,
            }
        )
        request.session = {'user_id': user_.id}
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "No scopes data attached."
        )

    def test_change_scopes_non_iterable_scope_data(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": app_.id,
                "scopes": 5
            }
        )
        request.session = {'user_id': user_.id}
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "Invalid scope data that could not be iterated."
        )

    def test_change_scopes_non_parsable_scope_data(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": app_.id,
                "scopes": "{}{}"
            }
        )
        request.session = {'user_id': user_.id}
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "Invalid scope data that could not be parsed."
        )

    def test_change_scopes_app_does_not_exist(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": 100000000000001,
                "scopes": "{}"
            }
        )
        request.session = {'user_id': user_.id}
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            content["message"],
            "App does not exist."
        )

    def test_change_scopes_success(self):
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")
        request = self.factory.post(
            '/api/updatescopes/',
            {
                "app_id": app_.id,
                "scopes": '[{"checked":true, "name":"timetable"}, \
                           {"checked":false, "name":"student_number"}]'
            }
        )
        request.session = {'user_id': user_.id}
        self.assertEqual(app_.scope.scope_number, 0)
        response = update_scopes(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            content["message"],
            "Scope successfully changed."
        )
        app_ = App.objects.filter(id=app_.id, user=user_.id)[0]
        self.assertEqual(app_.scope.scope_number, 2)

    def test_analytics_no_token_provided(self):
        endpoints = self.functions = {
            '/api/analytics/total': number_of_requests,
            '/api/analytics/quota': quota_remaining,
            # '/api/analytics/services': most_popular_service,
            # '/api/analytics/methods': most_popular_method,
            '/api/analytics/oauth/total': users_per_app,
            '/api/analytics/oauth/total_by_dept':
                users_per_app_by_dept
        }

        for url in endpoints:
            request = self.factory.get(
                url,
                {
                }
            )
            response = endpoints[url](request)
            content = json.loads(response.content.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(content["message"], "No token provided")

    def test_analytics_bad_token_provided(self):
        endpoints = self.functions = {
            '/api/analytics/total': number_of_requests,
            '/api/analytics/quota': quota_remaining,
        }

        for url in endpoints:
            request = self.factory.get(
                url,
                {
                    "token": "this-is-very-garbage"
                }
            )
            response = endpoints[url](request)
            content = json.loads(response.content.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(content["message"], "Token is invalid")

    def test_analytics_quota_non_existent_token_provided(self):
        request = self.factory.get(
            '/api/analytics/quota',
            {
                "token": "uclapi-user-nonexistenttoken"
            }
        )
        response = quota_remaining(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["message"], "Token is invalid")

    def test_analytics_num_requests_good_app_token_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        token = app_.api_token

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="roombookings",
                                   method="rooms",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="roombookings",
                                   method="rooms",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/total',
            {
                "token": token
            }
        )
        response = number_of_requests(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["num"], 2)

    def test_analytics_num_requests_zero_app_token_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        token = app_.api_token

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/total',
            {
                "token": token
            }
        )
        response = number_of_requests(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["num"], 0)

    def test_analytics_num_requests_good_oauth_token_flow(self):
        # Set up token
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope_ = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        token = OAuthToken.objects.create(app=app_, user=user_,
                                          scope=scope_)

        # Create some request objects

        _ = APICall.objects.create(app=app_, user=dev_,
                                   token_type="oauth",
                                   service="timetable",
                                   method="personal",
                                   queryparams="", token=token)

        _ = APICall.objects.create(app=app_, user=dev_,
                                   token_type="oauth",
                                   service="timetable",
                                   method="personal",
                                   queryparams="", token=token)

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/total',
            {
                "token": token.token
            }
        )
        response = number_of_requests(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["num"], 2)

    def test_analytics_num_requests_zero_oauth_token_flow(self):
        # Set up token
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope_ = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        token = OAuthToken.objects.create(app=app_, user=user_,
                                          scope=scope_)

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/total',
            {
                "token": token.token
            }
        )
        response = number_of_requests(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["num"], 0)

    def test_analytics_quota_good_oauth_token_flow(self):
        # Set up token
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope_ = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        token = OAuthToken.objects.create(app=app_, user=user_,
                                          scope=scope_)

        # Use decorator library to decrement quota

        throttle_api_call(token, "oauth")

        throttle_api_call(token, "oauth")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/quota',
            {
                "token": token.token
            }
        )
        response = quota_remaining(request)
        content = json.loads(response.content.decode())
        # Clean up redis
        self.r.delete("oauth:" + token.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["remaining"], 9998)

    def test_analytics_quota_zero_oauth_token_flow(self):
        # Set up token
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope_ = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        token = OAuthToken.objects.create(app=app_, user=user_,
                                          scope=scope_)

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/quota',
            {
                "token": token.token
            }
        )
        response = quota_remaining(request)
        content = json.loads(response.content.decode())
        # Clean up redis
        self.r.delete("oauth:" + token.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["remaining"], 10000)

    def test_analytics_quota_good_app_token_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="quota_test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        token = app_.api_token

        # Use decorator library to decrement quota
        throttle_api_call(app_, "general")
        throttle_api_call(app_, "general")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/quota',
            {
                "token": token
            }
        )
        response = quota_remaining(request)
        content = json.loads(response.content.decode())
        # Clean up redis
        self.r.delete(app_.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["remaining"], 9998)

    def test_analytics_quota_zero_app_token_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="quota_test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )

        app_ = App.objects.create(user=user_, name="An App")

        token = app_.api_token

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/quota',
            {
                "token": token
            }
        )
        response = quota_remaining(request)
        content = json.loads(response.content.decode())
        # Clean up redis
        self.r.delete(app_.user.email)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["remaining"], 10000)

    def test_analytics_most_popular_service_good_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="rooms",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="rooms",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service2",
                                   method="rooms",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/services',
            {}
        )
        response = most_popular_service(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [{'service': 'service1', 'count': 2},
                                           {'service': 'service2', 'count':
                                               1}])

    def test_analytics_most_popular_service_empty_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        _ = App.objects.create(user=user_, name="An App")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/services',
            {}
        )
        response = most_popular_service(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [])

    def test_analytics_most_popular_method_good_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service2",
                                   method="method2",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/methods',
            {}
        )
        response = most_popular_method(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [{'method': 'method1', 'count': 2},
                                           {'method': 'method2', 'count':
                                               1}])

    def test_analytics_most_popular_method_filter_by_service_good_flow(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service2",
                                   method="method2",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/methods',
            {
                "service": "service1"
            }
        )
        response = most_popular_method(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [{'method': 'method1', 'count': 2}])

    def test_analytics_most_popular_method_filter_by_service_empty_good_flow(
            self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        _ = App.objects.create(user=user_, name="An App")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/methods',
            {
                "service": "service1"
            }
        )
        response = most_popular_method(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [])

    def test_analytics_most_popular_method_alternate_split_services(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method2",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service2",
                                   method="method2",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/methods',
            {
                "split_services": "true"
            }
        )
        response = most_popular_method(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], {
            "service1": [
                {
                    "method": "method1",
                    "count": 2,
                },
                {
                    "method": "method2",
                    "count": 1,
                }
            ],
            "service2": [
                {
                    "method": "method2",
                    "count": 1,
                }
            ]
        })

    def test_analytics_most_popular_method_alternate_no_split_services(self):
        # Set up token
        user_ = User.objects.create(
            email="test@ucl.ac.uk",
            cn="test",
            given_name="Test Test"
        )
        app_ = App.objects.create(user=user_, name="An App")

        # Create some request objects
        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1/name1",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service1",
                                   method="method1/name2",
                                   queryparams="")

        _ = APICall.objects.create(app=app_, user=user_,
                                   token_type="general",
                                   service="service2",
                                   method="method2",
                                   queryparams="")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/methods',
            {
                "split_services": "false"
            }
        )
        response = most_popular_method(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [{'method': 'method1', 'count': 2},
                                           {'method': 'method2', 'count': 1}])

    def test_analytics_users_per_app_good_flow(self):
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        user2_ = User.objects.create(
            email="user2@ucl.ac.uk",
            cn="user2",
            given_name="Test Test",
            employee_id="3"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope1 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)
        scope2 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        _ = OAuthToken.objects.create(app=app_, user=user_,
                                      scope=scope1)

        _ = OAuthToken.objects.create(app=app_, user=user2_,
                                      scope=scope2)

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/oauth/total',
            {
                "token": app_.api_token
            }
        )
        response = users_per_app(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["users"], 2)

    def test_analytics_users_per_app_zero_flow(self):
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/oauth/total',
            {
                "token": app_.api_token
            }
        )
        response = users_per_app(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["users"], 0)

    def test_analytics_users_per_app_date_filter_good_flow(self):
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2"
        )

        user2_ = User.objects.create(
            email="user2@ucl.ac.uk",
            cn="user2",
            given_name="Test Test",
            employee_id="3"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope1 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)
        scope2 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        date1 = datetime.strptime("2020-12-15", "%Y-%m-%d")
        date2 = datetime.strptime("2010-12-15", "%Y-%m-%d")

        otoken1 = OAuthToken.objects.create(app=app_, user=user_,
                                            scope=scope1)
        otoken1.creation_date = date1
        otoken1.save()

        otoken2 = OAuthToken.objects.create(app=app_, user=user2_,
                                            scope=scope2)
        otoken2.creation_date = date2
        otoken2.save()

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/oauth/total',
            {
                "token": app_.api_token,
                "start_date": "2020-12-01",
                "end_date": "2020-12-30"
            }
        )
        response = users_per_app(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["users"], 1)

    def test_analytics_users_per_app_per_dept_good_flow(self):
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        user_ = User.objects.create(
            email="user@ucl.ac.uk",
            cn="user",
            given_name="Test Test",
            employee_id="2",
            department="dep1"
        )

        user2_ = User.objects.create(
            email="user2@ucl.ac.uk",
            cn="user2",
            given_name="Test Test",
            employee_id="3",
            department="dep2"
        )

        user3_ = User.objects.create(
            email="user3@ucl.ac.uk",
            cn="user3",
            given_name="Test Test",
            employee_id="4",
            department="dep2"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        scope1 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)
        scope2 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)
        scope3 = OAuthScope.objects.create(
            scope_number=app_.scope.scope_number)

        _ = OAuthToken.objects.create(app=app_, user=user_,
                                      scope=scope1)

        _ = OAuthToken.objects.create(app=app_, user=user2_,
                                      scope=scope2)

        _ = OAuthToken.objects.create(app=app_, user=user3_,
                                      scope=scope3)

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/oauth/total_by_dept',
            {
                "token": app_.api_token
            }
        )
        response = users_per_app_by_dept(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [{"department": "dep2", "count": 2},
                                           {"department": "dep1", "count": 1}])

    def test_analytics_users_per_app_per_dept_zero_flow(self):
        dev_ = User.objects.create(
            email="dev@ucl.ac.uk",
            cn="dev",
            given_name="Test Test",
            employee_id="1"
        )

        app_ = App.objects.create(user=dev_, name="An App")

        # Hit endpoint and check number is correct
        request = self.factory.get(
            '/api/analytics/oauth/total_by_dept',
            {
                "token": app_.api_token
            }
        )
        response = users_per_app_by_dept(request)
        content = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["data"], [])
