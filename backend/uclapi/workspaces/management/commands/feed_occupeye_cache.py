from django.core.management.base import BaseCommand

from workspaces.tasks import feed_occupeye_cache


class Command(BaseCommand):
    help = 'Caches all OccupEye data into Redis'

    def add_arguments(self, parser):
        parser.add_argument("--test", action='store_true')
        parser.add_argument("--mini", action='store_true')

    def handle(self, *args, **options):
        feed_occupeye_cache(options['test'], options['mini']).apply()
