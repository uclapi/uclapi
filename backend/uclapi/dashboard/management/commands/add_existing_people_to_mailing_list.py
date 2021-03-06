from django.core.management.base import BaseCommand

from dashboard.models import User
from dashboard.tasks import add_user_to_mailing_list


class Command(BaseCommand):

    help = 'Adds the signed up devs to the mailchimp  mailing list.'

    def handle(self, *args, **options):
        users = User.objects.filter(agreement=True)
        for user in users:
            add_user_to_mailing_list(user.email, user.full_name)
