from django.core.management.base import BaseCommand

from timetable.models import Lock


class Command(BaseCommand):

    help = 'creates the lock used to decide which bucket to flush and fill'

    def handle(self, *args, **options):
        # delete existing locks
        Lock.objects.all().delete()
        lock = Lock(a=True, b=False)
        lock.save()
        self.stdout.write("Created a lock")
