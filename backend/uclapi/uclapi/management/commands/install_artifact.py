from django.core.management.base import BaseCommand

import requests


class Command(BaseCommand):
    help = 'Installs frontend artifact files and updates statics'

    def add_arguments(self, parser):
        parser.add_argument('artifact_id', nargs=1, type=int)

    def handle(self, *args, **options):
        artifact_id = options['artifact_id']

        