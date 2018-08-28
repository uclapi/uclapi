from django.core.management.base import BaseCommand

from timetable.app_helpers import get_student_timetable


class Command(BaseCommand):

    help = 'Clones timetable related dbs to speed up queries'

    def handle(self, *args, **options):
        upi = input("Please enter the student UPI: ")
        tt = get_student_timetable(upi)
        print(tt)
