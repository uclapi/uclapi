import os

from binascii import hexlify
from distutils.util import strtobool

import redis

from django.conf import settings
from django.test import TestCase

from .occupeye.api import OccupEyeApi
from .occupeye.constants import OccupEyeConstants
from .occupeye.token import (
    get_bearer_token,
    token_valid
)


class OccupEyeApiTestCase(TestCase):
    def setUp(self):
        self.r = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self._consts = OccupEyeConstants()

        # Ensure we have no tokens in Redis yet
        self.r.delete(
            self._consts.ACCESS_TOKEN_KEY
        )
        self.r.delete(
            self._consts.ACCESS_TOKEN_EXPIRY_KEY
        )

        # Instantiate the OccupEye API in test mode
        self.api = OccupEyeApi()

    def test_tokens_empty(self):
        # The Redis get functions should return None values
        self.assertEqual(
            self.r.get(self._consts.ACCESS_TOKEN_KEY),
            None
        )
        self.assertEqual(
            self.r.get(self._consts.ACCESS_TOKEN_EXPIRY_KEY),
            None
        )

    def test_token_expiry(self):
        access_token = "blahblah"
        access_token_expiry = 1
        self.assertFalse(
            token_valid(access_token, access_token_expiry)
        )
        # 1st January 2100. I'd be honoured if this code is still
        # being run 83 years from now!
        access_token_expiry = 4102444800
        self.assertTrue(
            token_valid(access_token, access_token_expiry)
        )

    def test_bearer_token_generator(self):
        # Generate a random token then check that the bearer string
        # is properly formed
        random_data = hexlify(os.urandom(30)).decode()
        access_token = random_data
        access_token_expiry = 4102444800
        self.assertEqual(
            get_bearer_token(
                access_token,
                access_token_expiry,
                self._consts
            ),
            "Bearer " + random_data
        )

    def test_get_surveys(self):
        # Create some bogus surveys to test with
        pipeline = self.r.pipeline()
        pipeline.delete("occupeye:surveys")
        pipeline.delete("occupeye:surveys:9991")
        pipeline.delete("occupeye:surveys:9992")
        pipeline.lpush("occupeye:surveys", 9991)
        pipeline.lpush("occupeye:surveys", 9992)
        pipeline.hmset(
            "occupeye:surveys:9991",
            {
                "id": 9991,
                "active": str(True),
                "name": "test survey 1",
                "start_time": "10:00",
                "end_time": "12:00",
                "staff_survey": str(True),
                "lat": "3.14159",
                "long": "-0.500100",
                "address1": "some building",
                "address2": "some street",
                "address3": "some city",
                "address4": "postcode please"
            }
        )
        pipeline.hmset(
            "occupeye:surveys:9992",
            {
                "id": 9992,
                "active": str(False),
                "name": "test survey 2",
                "start_time": "09:00",
                "end_time": "17:00",
                "staff_survey": str(False),
                "lat": "2.14159",
                "long": "-1.500100",
                "address1": "some building2",
                "address2": "some street2",
                "address3": "some city2",
                "address4": "postcode please2"
            }
        )
        pipeline.expire("occupeye:surveys", 20)
        pipeline.expire("occupeye:surveys:9991", 20)
        pipeline.expire("occupeye:surveys:9992", 20)
        pipeline.execute()

        surveys = self.api.get_surveys("all")
        # When the data comes from the actual API it is backwards
        surveys.reverse()
        self.assertEqual(
            len(surveys),
            2
        )
        self.assertEqual(
            len(surveys[0]),
            8
        )

        self.assertEqual(
            surveys[0]["id"],
            9991
        )
        self.assertTrue(surveys[0]["active"])
        self.assertEqual(
            surveys[0]["name"],
            "test survey 1"
        )
        self.assertEqual(
            surveys[0]["start_time"],
            "10:00"
        )
        self.assertEqual(
            surveys[0]["end_time"],
            "12:00"
        )
        self.assertTrue(
            strtobool(str(surveys[0]["staff_survey"]))
        )
        self.assertEqual(
            surveys[0]["location"]["coordinates"]["lat"],
            "3.14159"
        )
        self.assertEqual(
            surveys[0]["location"]["coordinates"]["lng"],
            "-0.500100"
        )
        self.assertEqual(
            surveys[0]["location"]["address"][0],
            "some building"
        )
        self.assertEqual(
            surveys[0]["location"]["address"][1],
            "some street"
        )
        self.assertEqual(
            surveys[0]["location"]["address"][2],
            "some city"
        )
        self.assertEqual(
            surveys[0]["location"]["address"][3],
            "postcode please"
        )

        self.assertEqual(
            surveys[1]["id"],
            9992
        )
        self.assertFalse(surveys[1]["active"])
        self.assertEqual(
            surveys[1]["name"],
            "test survey 2"
        )
        self.assertEqual(
            surveys[1]["start_time"],
            "09:00"
        )
        self.assertEqual(
            surveys[1]["end_time"],
            "17:00"
        )
        self.assertFalse(
            strtobool(str(surveys[1]["staff_survey"]))
        )
        self.assertEqual(
            surveys[1]["location"]["coordinates"]["lat"],
            "2.14159"
        )
        self.assertEqual(
            surveys[1]["location"]["coordinates"]["lng"],
            "-1.500100"
        )
        self.assertEqual(
            surveys[1]["location"]["address"][0],
            "some building2"
        )
        self.assertEqual(
            surveys[1]["location"]["address"][1],
            "some street2"
        )
        self.assertEqual(
            surveys[1]["location"]["address"][2],
            "some city2"
        )
        self.assertEqual(
            surveys[1]["location"]["address"][3],
            "postcode please2"
        )
