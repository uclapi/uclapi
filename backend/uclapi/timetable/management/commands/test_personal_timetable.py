import time

from django.core.management.base import BaseCommand
import json

from timetable.app_helpers import get_student_timetable
from timetable.personal_timetable import get_personal_timetable


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def add_arguments(self, parser):
        parser.add_argument('upi')

    def handle(self, *args, **options):
        upi = options['upi']
        start_time = time.time()
        # tt = get_personal_timetable(upi)
        tt = get_student_timetable(upi)
        elapsed_time = time.time() - start_time
        print(json.dumps(tt))
