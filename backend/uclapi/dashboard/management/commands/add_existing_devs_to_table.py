from django.core.management.base import BaseCommand

from dashboard.models import User, Developer


class Command(BaseCommand):

    help = 'Adds already existing developers to Developer table.'

    def handle(self, *args, **options):
        for user in User.objects.filter(agreement=True):
            Developer(user=user).save()
