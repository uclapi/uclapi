from django.test import SimpleTestCase
from itertools import chain

from .helpers import _serialize_rooms, _serialize_equipment, _parse_datetime
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
        date_only = [
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
            ["2017-01-16T11:34:39+00:00", None, "334533"],
            ["2017-02-16T11:34:39+00:00", None, "334533"],
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
        ]

        self.assertEqual(

        )
