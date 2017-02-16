from django.test import SimpleTestCase
from itertools import chain

from .helpers import _serialize_rooms, _serialize_equipment
from .models import Room


class FakeModelClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class RoomSerializationTestCase(SimpleTestCase):

    def test_serialize_rooms(self):
        room_list = [
            FakeModelClass(
                sitename="South Quad Pop Up Learning Hub",
                address1="Gower St",
                address2="London",
                address3=None,
                address4=None,
                webview="Y",
                automated="N",
                roomid=118,
                siteid="X402",
                roomname="South Quad Pop Up Learning Hub 101",
                category="REC",
                bookabletype="CB",
                roomclass="CR",
                zone="NN",
                capacity=25,
                roomdeptid="ESTDV_ADM",
                setid="LIVE-17-18",
            ),
            FakeModelClass(
                sitename="Institute of Advanced Legal Studies",
                address1="Charles Clore House,17 Russell Square",
                address2="London",
                address3="WC1B 5DR",
                address4=None,
                webview="Y",
                automated="P",
                roomid=123123,
                siteid="X234324",
                roomname="Provost's Private Room",
                category="REC",
                bookabletype="CB",
                roomclass="CR",
                zone="YY",
                capacity=500,
                roomdeptid="ESTDV_ADM",
                setid="LIVE-16-17",
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
                    "sitename": "South Quad Pop Up Learning Hub",
                    "capacity": 25,
                    "classification": "CR",
                    "automated": "N",
                    "location": {
                        "address1": "Gower St",
                        "address2": "London",
                        "address3": None,
                        "address4": None
                    }
                },
                {
                    "name": "Provost's Private Room",
                    "roomid": 123123,
                    "siteid": "X234324",
                    "sitename": "Institute of Advanced Legal Studies",
                    "capacity": 500,
                    "classification": "CR",
                    "automated": "P",
                    "location": {
                        "address1": "Charles Clore House,17 Russell Square",
                        "address2": "London",
                        "address3": "WC1B 5DR",
                        "address4": None
                    }
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
