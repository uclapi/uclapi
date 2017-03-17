from django.core.management.base import BaseCommand
from datetime import datetime
import requests
import re
from roombookings.models import Location


class Command(BaseCommand):
    help = "Fetches lat lng coordinates from Estates and puts them in our db"

    def handle(self, *args, **options):

        starttime = datetime.now()

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
            '026'
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
                r'.*"http:\/\/streetmap.co.uk\/loc\/(.*),(.*)".*',
                r.text
            )
            if searchObj:
                lat = searchObj.group(1)
                lng = searchObj.group(2)

                location, created = Location.objects.get_or_create(
                    siteid=site_id
                )
                location.lat = lat
                location.lng = lng
                location.save()

        print("Total Time taken: ", datetime.now() - starttime)
        self.stdout.write("All done")
