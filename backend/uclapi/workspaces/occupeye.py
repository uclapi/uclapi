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
    # Keep survey data around in the cache for an hour
    SURVEY_TTL = 3600
    def __init__(self, test_mode=False):
        self.r = redis.StrictRedis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self.deployment_id = os.environ["OCCUPEYE_DEPLOYMENT_ID"]
        self.deployment_name = os.environ["OCCUPEYE_DEPLOYMENT_NAME"]
        self.base_url = os.environ["OCCUPEYE_BASE_URL"]

        # If either of those variables come up false, make sure
        # we have an access token before we continue.
        # We don't want to do anything manually in test mode to avoid
        # hitting environment variables we may not have yet.
        if test_mode:
            self.access_token = None
            self.access_token_expiry = None
        else:
            self.access_token = self.r.get("occupeye:access_token")

            access_token_expiry = self.r.get("occupeye:access_token_expiry")
            # We can only cast this value to an int if we know it's not None
            if access_token_expiry:
                self.access_token_expiry = int(access_token_expiry)
            else:
                self.access_token_expiry = None
            if not self.access_token or not self.access_token_expiry:
                self.get_token()

    def _str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

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
        self.r.set("occupeye:access_token", self.access_token)
        self.r.set("occupeye:access_token_expiry", self.access_token_expiry)

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

    def _cache_survey_data(self):
        # Use a Redis Pipeline to ensure that all the data is inserted together
        # and atomically
        pipeline = self.r.pipeline()
        # Ensure that the list of occupeye surveys has actually been cleared
        pipeline.delete("occupeye:surveys")

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
        surveys_data = request.json()

        for survey in surveys_data:
            survey_key = "occupeye:surveys:" + str(survey["SurveyID"])
            pipeline.hmset(
                survey_key,
                {
                    "id": survey["SurveyID"],
                    "active": survey["Active"],
                    "name": survey["Name"],
                    "start_time": survey["StartTime"],
                    "end_time": survey["EndTime"]
                }
            )
            pipeline.expire(survey_key, self.SURVEY_TTL)
            # We prepend to the list of Surveys because the API returns
            # a list of surveys where the ID decrements
            pipeline.lpush("occupeye:surveys", str(survey["SurveyID"]))

        pipeline.expire("occupeye:surveys", self.SURVEY_TTL)
        pipeline.execute()

    def get_surveys(self):
        if self.r.llen("occupeye:surveys") == 0:
            # The data is not in the cache, so cache it.
            self._cache_survey_data()

        # Now we know we have the data cached, we can serve it
        survey_ids = self.r.lrange(
            "occupeye:surveys",
            0,
            self.r.llen("occupeye:surveys") - 1
        )

        surveys = []

        for id in survey_ids:
            survey_data = self.r.hgetall("occupeye:surveys:" + id)
            surveys.append(
                {
                    "id": int(survey_data["id"]),
                    "name": survey_data["name"],
                    "active": self._str2bool(survey_data["active"]),
                    "start_time": survey_data["start_time"],
                    "end_time": survey_data["end_time"]
                }
            )

        return surveys
