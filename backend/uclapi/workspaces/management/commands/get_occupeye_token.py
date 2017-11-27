import json
import os
import redis
import requests
from time import time as time_now

from django.conf import settings
from django.core.management.base import BaseCommand


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
        # Connect to Redis first so that we can cache this key
        r = redis.StrictRedis(host=settings.REDIS_UCLAPI_HOST)

        url = os.environ["OCCUPEYE_BASE_URL"] + '/token'
        body = {
            "Grant_type": "password",
            "Username": os.environ["OCCUPEYE_USERNAME"],
            "Password": os.environ["OCCUPEYE_PASSWORD"]
        }

        request = requests.post(
            url=url,
            data=body
        )

        response = json.loads(request.text)
        r.set("OCCUPEYE_ACCESS_TOKEN", response["access_token"])
        r.set("OCCUPEYE_ACCESS_TOKEN_EXPIRY", int(time_now()) + int(response["expires_in"]))

        if not options['silent']:
            print("New token {} expires at {}".format(
                r.get("OCCUPEYE_ACCESS_TOKEN"),
                r.get("OCCUPEYE_ACCESS_TOKEN_EXPIRY")
            ))
