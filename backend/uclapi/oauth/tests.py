from django.test import TestCase

from .models import OAuthScope
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
