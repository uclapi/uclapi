from django.test import SimpleTestCase
from itertools import chain

from .helpers import _serialize_rooms, _serialize_equipment
from .models import Room


class FakeModelClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class SerializationTestCase(SimpleTestCase):

    def test_serialize_rooms(self):
        room_list = [
            FakeModelClass(
                roomid=118,
                siteid="X402",
                name="South Quad Pop Up Learning Hub 101",
                category="REC",
                type="CB",
                classification="CR",
                roomgrpcode="",
                zone="NN",
                capacity=25,
                prefmin="",
                prefmax="",
                deptid="ESTDV_ADM",
                roomarea=-1,
                dynafill="N",
                setid="LIVE-17-18",
                uniquefield="",
                linkcode="",
                campusid="X01"
            ),
            FakeModelClass(
                roomid=123123,
                siteid="X234324",
                name="Provost's Private Room",
                category="REC",
                type="CB",
                classification="CR",
                roomgrpcode="",
                zone="YY",
                capacity=500,
                prefmin="",
                prefmax="",
                deptid="ESTDV_ADM",
                roomarea=-1,
                dynafill="N",
                setid="LIVE-16-17",
                uniquefield="",
                linkcode="",
                campusid="X50"
            )
        ]
        none_qs = Room.objects.none()
        rooms_qs = list(chain(none_qs, room_list))
        serialised_rooms = _serialize_rooms(rooms_qs)
        self.assertEqual(
            serialised_rooms, [
                {
                    "name": "South Quad Pop Up Learning Hub 101",
                    "roomid": 118,
                    "siteid": "X402",
                    "capacity": 25,
                    "classification": "CR",
                    "zone": "NN"
                },
                {
                    "name": "Provost's Private Room",
                    "roomid": 123123,
                    "siteid": "X234324",
                    "capacity": 500,
                    "classification": "CR",
                    "zone": "YY"
                }
            ]
        )


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
