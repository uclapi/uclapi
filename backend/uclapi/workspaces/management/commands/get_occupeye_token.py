from django.core.management.base import BaseCommand

import redis

from django.conf import settings

from workspaces.occupeye import OccupEyeApi


class Command(BaseCommand):
    help = 'Gets a Cad-Capture OccupEye OAuth token and places it into Redis'

    def add_arguments(self, parser):
        parser.add_argument(
            '--silent',
            action='store_true',
            dest='silent',
            help='Do not output the data at the end'
        )

    def handle(self, *args, **options):
        api = OccupEyeApi()
        api.get_token()

        r = redis.Redis(host=settings.REDIS_UCLAPI_HOST)

        if not options['silent']:
            print("New token {} expires at {}".format(
                r.get("OCCUPEYE_ACCESS_TOKEN"),
                r.get("OCCUPEYE_ACCESS_TOKEN_EXPIRY")
            ))
