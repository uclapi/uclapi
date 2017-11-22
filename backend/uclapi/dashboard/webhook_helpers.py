import random
import datetime
from roombookings.helpers import _kloppify


def generate_booking(roomid, siteid, contact):
    now = datetime.datetime.now().replace(microsecond=0, second=0, minute=0)
    end = now + datetime.timedelta(hours=random.choice([1, 2]))
    booking = {
        "description": "FAKE BOOKING {}".format(random.choice(
            ["Careers", "Meeting", "Conference", "Lecture"]
        )),
        "contact": "Jane Doe",
        "roomid": "LG04",
        "siteid": "085",
        "roomname": "Bedford Way (26) LG04",
        "phone": None,
        "weeknumber": float(random.randint(1, 52)),
        "slotid": random.randint(2000000, 5000000),
        "start_time": _kloppify(
            datetime.datetime.strftime(
                now, "%Y-%m-%dT%H:%M:%S"), now
            ),
        "end_time": _kloppify(
            datetime.datetime.strftime(
                end, "%Y-%m-%dT%H:%M:%S"), end
            )
    }

    if roomid:
        booking["roomid"] = roomid

    if siteid:
        booking["siteid"] = siteid

    if contact:
        booking["contact"] = "{}{}".format(
            contact,
            random.choice(["", " Tech Society", " Miller"])
        )

    return booking


def generate_webhook_test_content(roomid, siteid, contact):
    content = {}

    top_level_content = random.randint(1, 3)
    if top_level_content == 1 or top_level_content == 3:
        content["bookings_added"] = []
    if top_level_content == 2 or top_level_content == 3:
        content["bookings_removed"] = []

    for second_level_key in content.keys():
        number_of_bookings = random.randint(1, 10)
        for i in range(number_of_bookings):
            content[second_level_key].append(
                generate_booking(roomid, siteid, contact)
            )

    return content
