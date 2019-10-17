import time

from django.core.management.base import BaseCommand
import json

from timetable.personal_timetable import get_personal_timetable


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def add_arguments(self, parser):
        parser.add_argument('upi')

    def handle(self, *args, **options):
        upi = options['upi']
        tt = get_personal_timetable(upi)
        print(json.dumps(tt))
