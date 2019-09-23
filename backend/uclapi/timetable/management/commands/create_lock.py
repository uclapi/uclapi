from django.core.management.base import BaseCommand

from timetable.models import Lock


class Command(BaseCommand):

    help = 'creates the lock used to decide which bucket to flush and fill'

    def handle(self, *args, **options):
        if Lock.objects.all().count() == 0:
            lock = Lock(a=True, b=False)
            lock.save()
            self.stdout.write("Created a lock")
        elif Lock.objects.all().count() == 1:
            self.stdout.write("Lock already exists")
        else:
            Lock_to_keep = Lock.objects.all()[0]
            Lock.objects.exclude(pk__in=list(Lock_to_keep)).delete()
            self.stdout.write("Deleted all but first lock")
