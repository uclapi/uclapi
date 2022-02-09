from celery import shared_task
from celery.exceptions import Ignore

from typing import Dict, Union
import os
import requests
import json
import redis

from uclapi.settings import REDIS_UCLAPI_HOST


@shared_task
def refresh_libcal_token():
    r: redis.Redis = redis.Redis(host=REDIS_UCLAPI_HOST,
                                 charset="utf-8",
                                 decode_responses=True)
    url: str = os.environ["LIBCAL_BASE_URL"] + "/1.1/oauth/token"
    body: Dict[str, str] = {
        "client_id": os.environ["LIBCAL_CLIENT_ID"],
        "client_secret": os.environ["LIBCAL_CLIENT_SECRET"],
        "grant_type": "client_credentials"
    }
    response: requests.Response = requests.post(url=url,
                                                data=body)
    if response.status_code != 200:
        raise Ignore()

    response_data: Dict[str, Union[str, int]] = json.loads(response.text)

    r.setex("libcal:token", response_data["expires_in"], value=response_data["access_token"])
