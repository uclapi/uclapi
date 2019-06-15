import time

from django.core.management.base import BaseCommand
import json

from timetable.personal_timetable import get_personal_timetable


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def handle(self, *args, **options):
        upi = input("Please enter the student UPI: ")
        start_time = time.time()
        tt = get_personal_timetable(upi)
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        print(json.dumps(tt))
