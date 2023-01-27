from unittest import TestCase
from parameterized import parameterized
from .utils import camelise, cameliser, underscore, underscorer, whitelist_fields

CAMEL_TO_UNDERSCORE = (
    ("product", "product"),
    ("specialGuest", "special_guest"),
    ("applicationController", "application_controller"),
    ("area51Controller", "area51_controller"),
)

CAMEL_TO_UNDERSCORE_WITHOUT_REVERSE = (
    ("HTMLTidy", "html_tidy"),
    ("HTMLTidyGenerator", "html_tidy_generator"),
    ("FreeBSD", "free_bsd"),
    ("HTML", "html"),
)


class TestCamelise(TestCase):
    @parameterized.expand(CAMEL_TO_UNDERSCORE)
    def test_camerlise(self, c, u):
        self.assertEqual(c, camelise(u))

    def test_camelise_with_uppercase(self):
        self.assertEqual('Capital', camelise('capital', True))

    def test_camelise_with_underscores(self):
        self.assertEqual("camelCase", camelise('Camel_Case'))


class TestCameliser(TestCase):
    def test_simple(self):
        input = {'html_tidy': 1, 'HTML': 2}
        expected = {'htmlTidy': 1, 'hTML': 2}
        self.assertDictEqual(expected, cameliser(input))

    def test_nested(self):
        input = {'html_tidy': {'free_bsd': 1}, 'HTML': 2}
        expected = {'htmlTidy': {'freeBsd': 1}, 'hTML': 2}
        self.assertDictEqual(expected, cameliser(input))

    def test_nested_list(self):
        data = {'html_tidy': [{'free_bsd': 1}, {'free_bsd': 2}], 'HTML': 2}
        expected = {'htmlTidy': [{'freeBsd': 1}, {'freeBsd': 2}], 'hTML': 2}
        self.assertDictEqual(expected, cameliser(data))


class TestUnderscore(TestCase):
    @parameterized.expand(CAMEL_TO_UNDERSCORE + CAMEL_TO_UNDERSCORE_WITHOUT_REVERSE)
    def test_underscore(self, c, u):
        self.assertEqual(u, underscore(c))


class TestUnderscorer(TestCase):
    def test_simple(self):
        input = {'htmlTidy': 1, 'html': 2}
        expected = {'html_tidy': 1, 'html': 2}
        self.assertDictEqual(expected, underscorer(input))

    def test_nested(self):
        input = {'htmlTidy': {'FreeBSD': 1}, 'html': 2}
        expected = {'html_tidy': {'free_bsd': 1}, 'html': 2}
        self.assertDictEqual(expected, underscorer(input))

    def test_nested_list(self):
        data = {'htmlTidy': [{'freeBsd': 1}, {'freeBsd': 2}], 'html': 2}
        expected = {'html_tidy': [{'free_bsd': 1}, {'free_bsd': 2}], 'html': 2}
        self.assertDictEqual(expected, underscorer(data))


class TestWhitelist(TestCase):
    def test_whitelist(self):
        whitelist = ['booking_id', 'arbitrary_field_name', 'field_not_in_data']
        data = {'booking_id': 1,
                'arbitrary_field_name': 2,
                'arbitrary_other_field_name': 3,
                'super_sensitive_data': 4}
        expected = {'booking_id': 1, 'arbitrary_field_name': 2}
        self.assertDictEqual(expected, whitelist_fields(data, whitelist))
