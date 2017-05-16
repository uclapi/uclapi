from django.core.management.base import BaseCommand
from roombookings.models import Lock


class Command(BaseCommand):

    help = 'creates the lock used to decide which bucket to flush and fill'

    def handle(self, *args, **options):
        # delete existing locks
        Lock.objects.all().delete()
        lock = Lock(
            bookingA=True,
            bookingB=False
        )
        lock.save()
        self.stdout.write("Created a lock")
