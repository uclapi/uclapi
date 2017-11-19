from django.core.management.base import BaseCommand

from dashboard.models import User
from dashboard.api_applications import add_user_to_mailing_list


class Command(BaseCommand):

    help = 'creates the lock used to decide which bucket to flush and fill'

    def handle(self, *args, **options):
        # delete existing locks
        users = User.objects.filter(agreement=True)
        for user in users:
            add_user_to_mailing_list(user.email, user.given_name)
