from django.core.management.base import BaseCommand

from workspaces.tasks import feed_occupeye_archive


class Command(BaseCommand):
    help = 'Surveys new historical OccupEye data into Postgres'

    def add_arguments(self, parser):
        parser.add_argument("--test", action='store_true')
        parser.add_argument("--delete", action='store_true')

    def handle(self, *args, **options):
        feed_occupeye_archive(options['test'], options['delete']).apply()
