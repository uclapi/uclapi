from django.core.management.base import BaseCommand
import time
from timetable.app_helpers import get_student_timetable
import json

class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def handle(self, *args, **options):
        upi = input("Please enter the student UPI: ")
        start_time = time.time()
        tt = get_student_timetable(upi)
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        with open('data.json', 'w') as outfile:
            json.dump(tt, outfile,indent=4)
