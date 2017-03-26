from django.core.management.base import BaseCommand
from roombookings.models import Location
import json


class Command(BaseCommand):
    help = "Fetches lat lng coordinates from Estates and puts them in our db"

    def handle(self, *args, **options):
        room_data = json.loads(open('data/rooms.json').read())

        for room in room_data:
