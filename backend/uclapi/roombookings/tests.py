import datetime
from itertools import chain

from django.test import SimpleTestCase
from freezegun import freeze_time

from .helpers import (PrettyJsonResponse, _parse_datetime,
                      _serialize_equipment, _serialize_rooms,
                      how_many_seconds_until_midnight)
from .models import Room


class FakeModelClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class EquipmentSerializationTestCase(SimpleTestCase):

        def test_serialize_equipment(self):
            equipment_list = [
                FakeModelClass(
                    setid="LIVE-16-17",
                    roomid="016",
                    units=1,
                    description="Chairs with Tables",
                    siteid="267",
                    type="FF"
                ),
                FakeModelClass(
                    setid="LIVE-16-17",
                    roomid="105",
                    units=1,
                    description="Software - Earth Sciences - self learning",
                    siteid="002",
                    type="FF"
                )
            ]
            none_qs = Room.objects.none()
            equipment_qs = list(chain(none_qs, equipment_list))
            serialised_equipment = _serialize_equipment(equipment_qs)
            self.assertEqual(
                serialised_equipment, [
                    {
                        "type": "FF",
                        "description": "Chairs with Tables",
                        "units": 1
                    },
                    {
                        "type": "FF",
                        "description": (
                            "Software - Earth Sciences"
                            " - self learning"
                        ),
                        "units": 1
                    }
                ]
            )


class ParseDateTimeTestCase(SimpleTestCase):
    def test_parse_datetime(self):
        arg_list = [
            # valid dates
            [None, None, "20160219"],
            [None, None, "20170320"],
            [None, None, "20171214"],
            [None, None, "20171008"],
            [None, None, "20170101"],
            [None, None, "20180101"],
            # invalid dates
            [None, None, "31001312"],
            [None, None, "20170229"],
            [None, None, "20172323"],
            [None, None, "20198989"],
            # only start time
            ["2017-05-16T11:34:39+00:00", None, "342453"],
            ["2017-01-16T23:34:39+00:00", None, "334533"],
            ["2017-02-16T11:34:39+00:00", None, "334533"],
            # only end time
            [None, "2017-01-16T23:34:39+00:00", "334533"],
            # invalid start and end
            ["2012-16T11:34:39+00:00", None, "334533"],
            [None, "23424", "324254"],
            # both end and start time
            ["2017-05-16T11:34:39+00:00", "2018-05-16T11:34:39+00:00", "3423"],
            ["2017-12-16T10:00:00+00:00", "2018-06-16T10:00:00+00:00", "3"],
        ]

        expected = [
            (datetime.datetime(2016, 2, 19, 0, 0, 1),
                datetime.datetime(2016, 2, 19, 23, 59, 59), True),
            (datetime.datetime(2017, 3, 20, 0, 0, 1),
                datetime.datetime(2017, 3, 20, 23, 59, 59), True),
            (datetime.datetime(2017, 12, 14, 0, 0, 1),
                datetime.datetime(2017, 12, 14, 23, 59, 59), True),
            (datetime.datetime(2017, 10, 8, 0, 0, 1),
                datetime.datetime(2017, 10, 8, 23, 59, 59), True),
            (datetime.datetime(2017, 1, 1, 0, 0, 1),
                datetime.datetime(2017, 1, 1, 23, 59, 59), True),
            (datetime.datetime(2018, 1, 1, 0, 0, 1),
                datetime.datetime(2018, 1, 1, 23, 59, 59), True),
            (-1, -1, False),
            (-1, -1, False),
            (-1, -1, False),
            (-1, -1, False),
            (datetime.datetime(2017, 5, 16, 12, 34, 39), None, True),
            (datetime.datetime(2017, 1, 16, 23, 34, 39), None, True),
            (datetime.datetime(2017, 2, 16, 11, 34, 39), None, True),
            (None, datetime.datetime(2017, 1, 16, 23, 34, 39), True),
            (-1, -1, False),
            (-1, -1, False),
            (datetime.datetime(2017, 5, 16, 12, 34, 39),
                datetime.datetime(2018, 5, 16, 12, 34, 39), True),
            (datetime.datetime(2017, 12, 16, 10, 0, 0),
                datetime.datetime(2018, 6, 16, 11, 0, 0), True)
        ]

        for index, args in enumerate(arg_list):
            self.assertEqual(
                expected[index],
                _parse_datetime(args[0], args[1], args[2])
            )


class PrettyPrintJsonTestCase(SimpleTestCase):
    def test_pretty_print(self):
        response = PrettyJsonResponse({"foo":"bar"})
        self.assertEqual(response.content.decode(), '{\n    "foo": "bar"\n}')


class SecondsUntilMidnightTestCase(SimpleTestCase):
    def test_seconds_until_midnight(self):
        arg_list = [
            "2017-05-29 23:59:59",
            "2017-05-29 00:00:00",
            "2017-05-29 00:00:01"
        ]

        expected = [
            1,
            0,
            86399
        ]

        for idx, arg in enumerate(arg_list):
            with freeze_time(arg):
                self.assertEqual(how_many_seconds_until_midnight(), expected[idx])
