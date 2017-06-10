from unittest.mock import patch

from django.test import TestCase

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
