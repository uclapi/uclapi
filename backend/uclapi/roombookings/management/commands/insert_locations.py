from django.core.management.base import BaseCommand
from roombookings.models import Location
import json


class Command(BaseCommand):
    help = "Fetches lat lng coordinates from Estates and puts them in our db"

    def handle(self, *args, **options):
        with open(
            'roombookings/management/commands/data/rooms.json', 'r'
        ) as f:
            room_data = json.loads(f.read())

        for room in room_data:
            siteid = room_data[room]["siteid"]
            roomid = room_data[room]["roomid"]
            lat = room_data[room][
                "location"]["coordinates"]["latitude"]
            lng = room_data[room][
                "location"]["coordinates"]["longitude"]

            new_location = Location(
                siteid=siteid,
                roomid=roomid,
                lat=lat,
                lng=lng
            )
            new_location.save()

        self.stdout.write("All done")
