from timetable.tasks import update_gencache_celery

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clones databases from Oracle into PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('--skip-run-check',
                            action='store_true',
                            dest='skip_run_check',
                            default=False,
                            help=('The gencache task will run even if there is still a job '
                                  'in progress according to Redis')
                            )

    def handle(self, *args, **options):
        update_gencache_celery(options['skip_run_check'])
