import json
import os
import sys
from typing import Union

from django.core.management.base import BaseCommand
import redis
import requests

from uclapi.settings import REDIS_UCLAPI_HOST


class Command(BaseCommand):
    help = ('Refreshes OAuth token for LibCal')

    def handle(self, *args, **options):
        r: redis.Redis = redis.Redis(
            host=REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        url: str = os.environ["LIBCAL_BASE_URL"] + "/1.1/oauth/token"
        body: dict[str, str] = {
            "client_id": os.environ["LIBCAL_CLIENT_ID"],
            "client_secret": os.environ["LIBCAL_CLIENT_SECRET"],
            "grant_type": "client_credentials"
        }
        response: requests.Response = requests.post(
            url=url,
            data=body
        )
        if response.status_code != 200:
            sys.exit(1)

        response_data: dict[str, Union[str, int]] = json.loads(response.text)

        r.setex("libcal:token", response_data["expires_in"], value=response_data["access_token"])
