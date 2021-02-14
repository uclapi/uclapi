from django.core.management.base import BaseCommand
from datetime import datetime
import requests
import re
from roombookings.models import Location, SiteLocation
import json


class Command(BaseCommand):
    help = (
        "puts room lat/lng in our db from rooms.json"
        "and fetches site location from esstates"
    )

    def handle(self, *args, **options):

        starttime = datetime.now()

        # room locations
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

            room_location, created = Location.objects.get_or_create(
                siteid=siteid,
                roomid=roomid,
                lat=lat,
                lng=lng
            )
            room_location.save()

        # site locations
        site_ids = [
            '016',
            '088',
            '035',
            '012',
            '013',
            '040',
            '131',
            '028',
            '374',
            '045',
            '350',
            '365',
            '050',
            '212',
            '085',
            '005',
            '363',
            '032',
            '042',
            '201',
            '180',
            '086',
            '014',
            '171',
            '025',
            'X402',
            '126',
            '029',
            '006',
            '044',
            '037',
            '003',
            '176',
            '090',
            '024',
            '067',
            '107',
            '002',
            '181',
            '235',
            '162',
            '026',
            '440',
            '281',
            '084',
            '086',
            '388',
            '175'
        ]

        estates_url = (
            "http://www.ucl.ac.uk/efd/roombooking"
            "/building-location/"
        )
        for site_id in site_ids:
            params = {
                "id": site_id
            }
            r = requests.get(estates_url, params=params)

            searchObj = re.search(
                r'.*"http:\/\/streetmap\.co\.uk\/loc\/(.*),(.*)".*',
                r.text
            )
            if site_id == "440":
                # New Quad Pop Up building
                location, created = SiteLocation.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = "51.524368"
                location.lng = "-0.133946"
                location.save()
            elif site_id == "180":

                location, created = SiteLocation.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = "51.5218725"
                location.lng = "-0.1305394"
                location.save()

            elif site_id == "181":

                location, created = SiteLocation.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = "51.5218725"
                location.lng = "-0.1305394"
                location.save()

            elif site_id == "X402":

                location, created = SiteLocation.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = "51.523892"
                location.lng = "-0.133098"
                location.save()

            elif site_id == "RUS26":

                location, created = SiteLocation.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = "51.521831"
                location.lng = "-0.128202"
                location.save()

            else:

                if searchObj:
                    lat = searchObj.group(1)
                    lng = searchObj.group(2)

                    location, created = SiteLocation.objects.get_or_create(
                        siteid=site_id
                    )
                    location.lat = lat
                    location.lng = lng
                    location.save()
                else:
                    print(site_id)

        print("Total Time taken: ", datetime.now() - starttime)
        self.stdout.write("All done")
