from django.http import QueryDict
from django.test import SimpleTestCase

from .app_helpers import (
    validate_amp_query_params,
    _is_instance_in_criteria
)
from .amp import (
    InvalidAMPCodeException,
    ModuleInstance,
    STUDENT_TYPES
)


class AmpCodeParsing(SimpleTestCase):
    def test_real_code_regular_1(self):
        instance = ModuleInstance("A6U-T1")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['A']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            6
        )
        self.assertTrue(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": True,
                    "term_2": False,
                    "term_3": False,
                    "term_1_next_year": False,
                    "summer": False
                },
                "year_long": False,
                "lsr": False,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_regular_2(self):
        instance = ModuleInstance("C5P-T2/3")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['C']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            5
        )
        self.assertFalse(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": False,
                    "term_2": True,
                    "term_3": True,
                    "term_1_next_year": False,
                    "summer": False
                },
                "year_long": False,
                "lsr": False,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_lsr_1(self):
        instance = ModuleInstance("D5U-LSR")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['D']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            5
        )
        self.assertTrue(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": False,
                    "term_2": False,
                    "term_3": False,
                    "term_1_next_year": False,
                    "summer": False
                },
                "year_long": False,
                "lsr": True,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_lsr_2(self):
        instance = ModuleInstance("C6P-LSR")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['C']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            6
        )
        self.assertFalse(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": False,
                    "term_2": False,
                    "term_3": False,
                    "term_1_next_year": False,
                    "summer": False
                },
                "year_long": False,
                "lsr": True,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_year_long(self):
        instance = ModuleInstance("D6P-YEAR")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['D']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            6
        )
        self.assertFalse(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": True,
                    "term_2": True,
                    "term_3": True,
                    "term_1_next_year": False,
                    "summer": False
                },
                "year_long": True,
                "lsr": False,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_t234_1(self):
        instance = ModuleInstance("A6U-T2/3/4")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['A']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            6
        )
        self.assertTrue(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": False,
                    "term_2": True,
                    "term_3": True,
                    "term_1_next_year": False,
                    "summer": True
                },
                "year_long": False,
                "lsr": False,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_real_code_t234_2(self):
        instance = ModuleInstance("D6P-T2/3/4")
        self.assertEqual(
            instance.delivery.student_type,
            STUDENT_TYPES['D']
        )
        self.assertEqual(
            instance.delivery.fheq_level,
            6
        )
        self.assertFalse(instance.delivery.undergraduate)
        self.assertDictEqual(
            instance.periods.get_periods(),
            {
                "teaching_periods": {
                    "term_1": False,
                    "term_2": True,
                    "term_3": True,
                    "term_1_next_year": False,
                    "summer": True
                },
                "year_long": False,
                "lsr": False,
                "summer_school": {
                    "is_summer_school": False,
                    "sessions": {
                        "session_1": False,
                        "session_2": False
                    }
                }
            }
        )

    def test_invalid_code_1(self):
        with self.assertRaises(InvalidAMPCodeException):
            ModuleInstance("Z6P-T1")

    def test_invalid_code_2(self):
        with self.assertRaises(InvalidAMPCodeException):
            ModuleInstance("AA1P-T1")

    def test_invalid_code_3(self):
        with self.assertRaises(InvalidAMPCodeException):
            ModuleInstance("A7P-T5")

    def test_invalid_code_4(self):
        with self.assertRaises(InvalidAMPCodeException):
            ModuleInstance("A6U-Z2")

    def test_batch_amp_codes(self):
        test_codes = [
            "C5U-T3",
            "D5U-T3",
            "A5U-T4",
            "B5U-T4",
            "C5U-T4",
            "D5U-T4",
            "A5U-T1/2",
            "B5U-T1/2",
            "C5U-T1/2",
            "D5U-T1/2",
            "A5U-T2/3",
            "B5U-T2/3",
            "C5U-T2/3",
            "D5U-T2/3",
            "A5U-T2/3/4",
            "B5U-T2/3/4",
            "C5U-T2/3/4",
            "D5U-T2/3/4",
            "A5U-T3/4",
            "B5U-T3/4",
            "C5U-T3/4",
            "D5U-T3/4",
            "A6U-T1/2/3",
            "B6U-T1/2/3",
            "C6U-T1/2/3",
            "D6U-T1/2/3",
            "A6U-YEAR",
            "B6U-YEAR",
            "C6U-YEAR",
            "D6U-YEAR",
            "A6U-LSR",
            "B6U-LSR",
            "C6U-LSR",
            "D6U-LSR",
            "A6U-T1",
            "B6U-T1",
            "C6U-T1",
            "D6U-T1",
            "A6U-T2",
            "B6U-T2",
            "C6U-T2",
            "D6U-T2",
            "A6U-T3",
            "B6U-T3",
            "C6U-T3",
            "D6U-T3",
            "A6U-T4",
            "B6U-T4",
            "C6U-T4",
            "D6U-T4",
            "A6U-T1/2",
            "B6U-T1/2",
            "C6U-T1/2",
            "D6U-T1/2",
            "A6U-T2/3",
            "B6U-T2/3",
            "C6U-T2/3",
            "D6U-T2/3",
            "A6U-T2/3/4",
            "B6U-T2/3/4",
            "C6U-T2/3/4",
            "D6U-T2/3/4",
            "A6U-T3/4",
            "B6U-T3/4",
            "C6U-T3/4",
            "D6U-T3/4",
            "A7U-T1/2/3",
            "B7U-T1/2/3",
            "C7U-T1/2/3",
            "D7U-T1/2/3",
            "A7U-YEAR",
            "B7U-YEAR",
            "C7U-YEAR",
            "D7U-YEAR",
            "A7U-LSR",
            "B7U-LSR",
            "C7U-LSR",
            "D7U-LSR",
            "A7U-T1",
            "B7U-T1",
            "C7U-T1",
            "D7U-T1",
            "A7U-T2",
            "B7U-T2",
            "C7U-T2",
            "D7U-T2",
            "A7U-T3",
            "B7U-T3",
            "C7U-T3",
            "D7U-T3",
            "A7U-T4",
            "B7U-T4",
            "C7U-T4",
            "D7U-T4",
            "A7U-T1/2",
            "B7U-T1/2",
            "C7U-T1/2",
            "D7U-T1/2",
            "A7U-T2/3",
            "B7U-T2/3",
            "C7U-T2/3",
            "D7U-T2/3",
            "A7U-T2/3/4",
            "B7U-T2/3/4",
            "C7U-T2/3/4",
            "D7U-T2/3/4",
            "A7U-T3/4",
            "B7U-T3/4",
            "C7U-T3/4",
            "D4P-T2",
            "A4P-T3",
            "D7U-T3/4",
            "A8U-T1/2/3",
            "B8U-T1/2/3",
            "C8U-T1/2/3",
            "D8U-T1/2/3",
            "A8U-YEAR",
            "B8U-YEAR",
            "C8U-YEAR",
            "D8U-YEAR",
            "A8U-LSR",
            "B8U-LSR",
            "C8U-LSR",
            "D8U-LSR",
            "A8U-T1",
            "B8U-T1",
            "C8U-T1",
            "D8U-T1",
            "A8U-T2",
            "B8U-T2",
            "C8U-T2",
            "D8U-T2",
            "A8U-T3",
            "B8U-T3",
            "C8U-T3",
            "D8U-T3",
            "A8U-T4",
            "B8U-T4",
            "C8U-T4",
            "D8U-T4",
            "A8U-T1/2",
            "B8U-T1/2",
            "C8U-T1/2",
            "D8U-T1/2",
            "A8U-T2/3",
            "B8U-T2/3",
            "C8U-T2/3",
            "D8U-T2/3",
            "A8U-T2/3/4",
            "B8U-T2/3/4",
            "C8U-T2/3/4",
            "D8U-T2/3/4",
            "A8U-T3/4",
            "B8U-T3/4",
            "C8U-T3/4",
            "D8U-T3/4",
            "A0P-T1/2/3",
            "B0P-T1/2/3",
            "C0P-T1/2/3",
            "D0P-T1/2/3",
            "A0P-YEAR",
            "B0P-YEAR",
            "C0P-YEAR",
            "D0P-YEAR",
            "A0P-LSR",
            "B0P-LSR",
            "C0P-LSR",
            "D0P-LSR",
            "A0P-T1",
            "B0P-T1",
            "C0P-T1",
            "D0P-T1",
            "A0P-T2",
            "B0P-T2",
            "C0P-T2",
            "D0P-T2",
            "A0P-T3",
            "B0P-T3",
            "C0P-T3",
            "D0P-T3",
            "A0P-T4",
            "B0P-T4",
            "C0P-T4",
            "D0P-T4",
            "A0P-T1/2",
            "B0P-T1/2",
            "C0P-T1/2",
            "D0P-T1/2",
            "A0P-T2/3",
            "B0P-T2/3",
            "C0P-T2/3",
            "D0P-T2/3",
            "A0P-T2/3/4",
            "B0P-T2/3/4",
            "C0P-T2/3/4",
            "D0P-T2/3/4",
            "A0P-T3/4",
            "B0P-T3/4",
            "C0P-T3/4",
            "D0P-T3/4",
            "A4P-T1/2/3",
            "B4P-T1/2/3",
            "C4P-T1/2/3",
            "D4P-T1/2/3",
            "A4P-YEAR",
            "B4P-YEAR",
            "C4P-YEAR",
            "D4P-YEAR",
            "A4P-LSR",
            "B4P-LSR",
            "C4P-LSR",
            "D4P-LSR",
            "A4P-T1",
            "B4P-T1",
            "C4P-T1",
            "D4P-T1",
            "A4P-T2",
            "B4P-T2",
            "C4P-T2",
            "B4P-T3",
            "C4P-T3",
            "D4P-T3",
            "A4P-T4",
            "B4P-T4",
            "C4P-T4",
            "D4P-T4",
            "A4P-T1/2",
            "B4P-T1/2",
            "C4P-T1/2",
            "D4P-T1/2",
            "A4P-T2/3",
            "B4P-T2/3",
            "C4P-T2/3",
            "D4P-T2/3",
            "A4P-T2/3/4",
            "B4P-T2/3/4",
            "C4P-T2/3/4",
            "D4P-T2/3/4",
            "A4P-T3/4",
            "B4P-T3/4",
            "C4P-T3/4",
            "D4P-T3/4",
            "A5P-T1/2/3",
            "B5P-T1/2/3",
            "C5P-T1/2/3",
            "D5P-T1/2/3",
            "A5P-YEAR",
            "B5P-YEAR",
            "C5P-YEAR",
            "D5P-YEAR",
            "A5P-LSR",
            "B5P-LSR",
            "C5P-LSR",
            "D5P-LSR",
            "A5P-T1",
            "B5P-T1",
            "C5P-T1",
            "D5P-T1",
            "A5P-T2",
            "B5P-T2",
            "C5P-T2",
            "D5P-T2",
            "A5P-T3",
            "B5P-T3",
            "C5P-T3",
            "D5P-T3",
            "A5P-T4",
            "B5P-T4",
            "C5P-T4",
            "D5P-T4",
            "A5P-T1/2",
            "B5P-T1/2",
            "C5P-T1/2",
            "D5P-T1/2",
            "A5P-T2/3",
            "B5P-T2/3",
            "C5P-T2/3",
            "D5P-T2/3",
            "A5P-T2/3/4",
            "B5P-T2/3/4",
            "C5P-T2/3/4",
            "D5P-T2/3/4",
            "A5P-T3/4",
            "B5P-T3/4",
            "C5P-T3/4",
            "D5P-T3/4",
            "A6P-T1/2/3",
            "B6P-T1/2/3",
            "C6P-T1/2/3",
            "D6P-T1/2/3",
            "A6P-YEAR",
            "B6P-YEAR",
            "C6P-YEAR",
            "D6P-YEAR",
            "A6P-LSR",
            "B6P-LSR",
            "C6P-LSR",
            "D6P-LSR",
            "A6P-T1",
            "B6P-T1",
            "C6P-T1",
            "D6P-T1",
            "A6P-T2",
            "B6P-T2",
            "C6P-T2",
            "D6P-T2",
            "A6P-T3",
            "B6P-T3",
            "C6P-T3",
            "D6P-T3",
            "A6P-T4",
            "B6P-T4",
            "C6P-T4",
            "D6P-T4",
            "A6P-T1/2",
            "B6P-T1/2",
            "C6P-T1/2",
            "D6P-T1/2",
            "A6P-T2/3",
            "B6P-T2/3",
            "C6P-T2/3",
            "D6P-T2/3",
            "A6P-T2/3/4",
            "B6P-T2/3/4",
            "C6P-T2/3/4",
            "D6P-T2/3/4",
            "A6P-T3/4",
            "B6P-T3/4",
            "C6P-T3/4",
            "D6P-T3/4",
            "A0U-T1/2/3",
            "B0U-T1/2/3",
            "C0U-T1/2/3",
            "D0U-T1/2/3",
            "A0U-YEAR",
            "B0U-YEAR",
            "C0U-YEAR",
            "D0U-YEAR",
            "A0U-LSR",
            "B0U-LSR",
            "C0U-LSR",
            "D0U-LSR",
            "A0U-T1",
            "B0U-T1",
            "C0U-T1",
            "D0U-T1",
            "A0U-T2",
            "B0U-T2",
            "C0U-T2",
            "D0U-T2",
            "A0U-T3",
            "B0U-T3",
            "C0U-T3",
            "D0U-T3",
            "A0U-T4",
            "B0U-T4",
            "C0U-T4",
            "D0U-T4",
            "A0U-T1/2",
            "B0U-T1/2",
            "C0U-T1/2",
            "D0U-T1/2",
            "A0U-T2/3",
            "B0U-T2/3",
            "C0U-T2/3",
            "D0U-T2/3",
            "A0U-T2/3/4",
            "B0U-T2/3/4",
            "C0U-T2/3/4",
            "D0U-T2/3/4",
            "A0U-T3/4",
            "B0U-T3/4",
            "C0U-T3/4",
            "D0U-T3/4",
            "A4U-T1/2/3",
            "B4U-T1/2/3",
            "C4U-T1/2/3",
            "D4U-T1/2/3",
            "A4U-YEAR",
            "B4U-YEAR",
            "C4U-YEAR",
            "D4U-YEAR",
            "A4U-LSR",
            "B4U-LSR",
            "C4U-LSR",
            "D4U-LSR",
            "A4U-T1",
            "B4U-T1",
            "C4U-T1",
            "D4U-T1",
            "A4U-T2",
            "B4U-T2",
            "C4U-T2",
            "D4U-T2",
            "A4U-T3",
            "B4U-T3",
            "C4U-T3",
            "D4U-T3",
            "A4U-T4",
            "B4U-T4",
            "C4U-T4",
            "D4U-T4",
            "A4U-T1/2",
            "B4U-T1/2",
            "C4U-T1/2",
            "D4U-T1/2",
            "A4U-T2/3",
            "B4U-T2/3",
            "C4U-T2/3",
            "D4U-T2/3",
            "A4U-T2/3/4",
            "B4U-T2/3/4",
            "C4U-T2/3/4",
            "D4U-T2/3/4",
            "A4U-T3/4",
            "B4U-T3/4",
            "C4U-T3/4",
            "D4U-T3/4",
            "A5U-T1/2/3",
            "B5U-T1/2/3",
            "C5U-T1/2/3",
            "D5U-T1/2/3",
            "A5U-YEAR",
            "B5U-YEAR",
            "C5U-YEAR",
            "D5U-YEAR",
            "A5U-LSR",
            "B5U-LSR",
            "C5U-LSR",
            "D5U-LSR",
            "A5U-T1",
            "B5U-T1",
            "C5U-T1",
            "D5U-T1",
            "A5U-T2",
            "B5U-T2",
            "C5U-T2",
            "D5U-T2",
            "A5U-T3",
            "B5U-T3",
            "D5P-T3/1",
            "A6U-T3/1",
            "A6P-T3/1",
            "B6U-T3/1",
            "B6P-T3/1",
            "C6U-T3/1",
            "C6P-T3/1",
            "D6U-T3/1",
            "D6P-T3/1",
            "A7U-T3/1",
            "A7P-T3/1",
            "B7U-T3/1",
            "B7P-T3/1",
            "C7U-T3/1",
            "C7P-T3/1",
            "D7U-T3/1",
            "D7P-T3/1",
            "A8U-T3/1",
            "A8P-T3/1",
            "B8U-T3/1",
            "B8P-T3/1",
            "C8U-T3/1",
            "C8P-T3/1",
            "D8U-T3/1",
            "D8P-T3/1",
            "A4U-T1/3",
            "A3U-T2",
            "A3U-T1",
            "A3U-T1/2",
            "A3P-T1",
            "A7P-T1/3",
            "A7P-T2/3/S",
            "A7P-T3/S",
            "B7P-T2/3/S",
            "D7P-T2/3/S",
            "A4U-S1",
            "A5U-S2",
            "A7P-T1/2/3",
            "B7P-T1/2/3",
            "C7P-T1/2/3",
            "D7P-T1/2/3",
            "A7P-YEAR",
            "B7P-YEAR",
            "C7P-YEAR",
            "D7P-YEAR",
            "A7P-LSR",
            "B7P-LSR",
            "C7P-LSR",
            "D7P-LSR",
            "A7P-T1",
            "B7P-T1",
            "C7P-T1",
            "D7P-T1",
            "A7P-T2",
            "B7P-T2",
            "C7P-T2",
            "D7P-T2",
            "A7P-T3",
            "B7P-T3",
            "C7P-T3",
            "D7P-T3",
            "A7P-T4",
            "B7P-T4",
            "C7P-T4",
            "D7P-T4",
            "A7P-T1/2",
            "B7P-T1/2",
            "C7P-T1/2",
            "D7P-T1/2",
            "A7P-T2/3",
            "B7P-T2/3",
            "C7P-T2/3",
            "D7P-T2/3",
            "A7P-T2/3/4",
            "B7P-T2/3/4",
            "C7P-T2/3/4",
            "D7P-T2/3/4",
            "A7P-T3/4",
            "B7P-T3/4",
            "C7P-T3/4",
            "D7P-T3/4",
            "A8P-T1/2/3",
            "B8P-T1/2/3",
            "C8P-T1/2/3",
            "D8P-T1/2/3",
            "A8P-YEAR",
            "B8P-YEAR",
            "C8P-YEAR",
            "D8P-YEAR",
            "A8P-LSR",
            "B8P-LSR",
            "C8P-LSR",
            "D8P-LSR",
            "A8P-T1",
            "B8P-T1",
            "C8P-T1",
            "D8P-T1",
            "A8P-T2",
            "B8P-T2",
            "C8P-T2",
            "D8P-T2",
            "A8P-T3",
            "B8P-T3",
            "C8P-T3",
            "D8P-T3",
            "A8P-T4",
            "B8P-T4",
            "C8P-T4",
            "D8P-T4",
            "A8P-T1/2",
            "B8P-T1/2",
            "C8P-T1/2",
            "D8P-T1/2",
            "A8P-T2/3",
            "B8P-T2/3",
            "C8P-T2/3",
            "D8P-T2/3",
            "A8P-T2/3/4",
            "B8P-T2/3/4",
            "C8P-T2/3/4",
            "D8P-T2/3/4",
            "A8P-T3/4",
            "B8P-T3/4",
            "C8P-T3/4",
            "D8P-T3/4",
            "A0U-T3/1",
            "A0P-T3/1",
            "B0U-T3/1",
            "B0P-T3/1",
            "C0U-T3/1",
            "C0P-T3/1",
            "D0U-T3/1",
            "D0P-T3/1",
            "A4U-T3/1",
            "A4P-T3/1",
            "B4U-T3/1",
            "B4P-T3/1",
            "C4U-T3/1",
            "C4P-T3/1",
            "D4U-T3/1",
            "D4P-T3/1",
            "A5U-T3/1",
            "A5P-T3/1",
            "B5U-T3/1",
            "B5P-T3/1",
            "C5U-T3/1",
            "C5P-T3/1",
            "D5U-T3/1"
        ]
        for code in test_codes:
            # We should not get an error for any of these codes
            ModuleInstance(code)


class AmpQueryParams(SimpleTestCase):
    """Tests for instance (AMP) query parameters"""

    def test_amp_params_are_correctly_validated(self):
        amp_params = [
            'term_1', 'term_2', 'term_3', 'term_1_next_year',
            'summer', 'is_summer_school', 'session_1',
            'session_2', 'lsr', 'year_long', 'is_undergraduate'
        ]
        valid_bools = ['0', '1', 'true', 'false']
        invalid_bools = ['maybe']
        for valid_bool in valid_bools:
            for amp_param in amp_params:
                query_params = QueryDict('{}={}'.format(amp_param,
                                                        valid_bool))
                self.assertTrue(validate_amp_query_params(query_params))

        for invalid_bool in invalid_bools:
            for amp_param in amp_params:
                query_params = QueryDict('{}={}'.format(amp_param,
                                                        invalid_bool))
                self.assertFalse(validate_amp_query_params(query_params))

        query_params = QueryDict('fheq_level=4')
        self.assertTrue(validate_amp_query_params(query_params))

        query_params = QueryDict('fheq_level=s')
        self.assertFalse(validate_amp_query_params(query_params))

    def test_instance_in_amp_params(self):
        criteria = QueryDict(mutable=True)
        amp_params = [
            'term_1', 'term_2', 'term_3', 'term_1_next_year',
            'summer', 'is_summer_school', 'session_1', 'session_2',
            'lsr', 'year_long', 'is_undergraduate', 'fheq_level'
        ]
        num_params = len(amp_params)
        amp_codes = [
            'A6U-T1',
            'B8P-YEAR'
        ]
        expected_bools = [
            [
                True, False, False, False,
                False, False, False, False,
                False, False, True, True
            ],
            [
                True, True, True, False,
                False, False, False, False,
                False, True, False, True
            ]
        ]
        expected_fheq_level = [6, 8]
        for x in range(len(amp_codes)):
            expected_bool = expected_bools[x]
            instance_obj = ModuleInstance(amp_codes[x])
            instance_dict = {
                "delivery": instance_obj.delivery.get_delivery(),
                "periods": instance_obj.periods.get_periods(),
                "instance_code": amp_codes[x]
            }
            for i in range(num_params-1):
                criteria[amp_params[i]] = 'true'
                self.assertEqual(_is_instance_in_criteria(instance_dict,
                                                          criteria),
                                 expected_bool[i])
                criteria[amp_params[i]] = 'false'
                self.assertNotEqual(_is_instance_in_criteria(instance_dict,
                                                             criteria),
                                    expected_bool[i])
                criteria.pop(amp_params[i])
            criteria['fheq_level'] = '0' + str(expected_fheq_level[x])
            self.assertEqual(_is_instance_in_criteria(instance_dict,
                                                      criteria),
                             expected_bool[num_params-1])
            criteria['fheq_level'] = '0' + str(expected_fheq_level[x] + 2)
            self.assertNotEqual(_is_instance_in_criteria(instance_dict,
                                                         criteria),
                                expected_bool[num_params-1])
