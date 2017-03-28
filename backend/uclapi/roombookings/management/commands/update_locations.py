from django.core.management.base import BaseCommand
from roombookings.models import Location
import json
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Fetches lat lng coordinates from Estates and puts them in our db"

    def handle(self, *args, **options):
        with open(
            'roombookings/management/commands/data/rooms.json', 'r'
        ) as f:
            room_data = json.loads(f.read())

        for room in room_data:
            siteid = room_data[room]["siteid"]
            lat = room_data[room][
                "location"]["coordinates"]["latitute"]
            lng = room_data[room][
                "location"]["coordinates"]["longitude"]
            try:
                loc = Location.objects.get(siteid=siteid)
                loc.lat = lat
                loc.lng = lng
                loc.save()
            except ObjectDoesNotExist:
                loc = Location(
                    siteid=siteid,
                    lat=lat,
                    lng=lng
                )
                loc.save()
        self.stdout.write("All done")
