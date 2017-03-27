from django.core.management.base import BaseCommand
from roombookings.models import Location
import json
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = "Fetches lat lng coordinates from Estates and puts them in our db"

    def handle(self, *args, **options):
        room_data = json.loads(open('roombookings/management/commands/data/rooms.json').read())

        for room in room_data:
            siteid = room_data[room]["siteid"]
            try:
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
            except:
                pass
        self.stdout.write("All done")
