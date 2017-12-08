import json
import os
from time import time as time_now
import redis
import requests

from django.conf import settings


class OccupEyeApi():
    """
    Python API for the Cad-Capture OccupEye backend.
    Data is cached as much as possible in Redis for performance.
    """
    def __init__(self, test_mode=False):
        self.r = redis.StrictRedis(host=settings.REDIS_UCLAPI_HOST)
        self.deployment_id = os.environ["OCCUPEYE_DEPLOYMENT_ID"]
        self.deployment_name = os.environ["OCCUPEYE_DEPLOYMENT_NAME"]
        self.base_url = os.environ["OCCUPEYE_BASE_URL"]

        self.access_token = self.r.get("OCCUPEYE_ACCESS_TOKEN")
        self.access_token_expiry = self.r.get("OCCUPEYE_ACCESS_TOKEN_EXPIRY")

        # If either of those variables come up false, make sure
        # we have an access token before we continue.
        # We don't want to do anything manually in test mode to avoid
        # hitting environment variables we may not have yet.
        if not test_mode:
            if not self.access_token or not self.access_token_expiry:
                self.get_token()

    def get_token(self):
        url = self.base_url + "/token"
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

        self.access_token = response["access_token"]
        self.access_token_expiry = int(time_now()) + int(response["expires_in"])
        self.r.set("OCCUPEYE_ACCESS_TOKEN", self.access_token)
        self.r.set("OCCUPEYE_ACCESS_TOKEN_EXPIRY", self.access_token_expiry)

    def token_valid(self):
        if not self.access_token:
            return False

        # Ensure the access token has not expired since we last checked
        if time_now() > self.access_token_expiry:
            return False

        return True

    def get_bearer_token(self):
        if not self.token_valid():
            self.get_token()

        return "Bearer " + self.access_token

    def get_surveys(self):
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/Surveys/?deployment={}".format(
            self.base_url,
            self.deployment_name
        )
        request = requests.get(
            url=url,
            headers=headers
        )
        surveys = request.json()
        return surveys
