import os
from binascii import hexlify

import redis

from django.conf import settings
from django.test import TestCase

from .occupeye import OccupEyeApi


class OccupEyeApiTestCase(TestCase):
    def setUp(self):
        self.r = redis.StrictRedis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )

        # Ensure we have no tokens in Redis yet
        self.r.delete("occupeye:access_token")
        self.r.delete("occupeye:access_token_expiry")

        # Instantiate the OccupEye API in test mode
        self.api = OccupEyeApi(test_mode=True)

    def test_tokens_empty(self):
        # The Redis get functions should return None values
        self.assertEqual(self.api.access_token, None)
        self.assertEqual(self.api.access_token_expiry, None)

    def test_token_expiry(self):
        self.api.access_token = "blahblah"
        self.api.access_token_expiry = 1
        self.assertFalse(
            self.api.token_valid()
        )
        # 1st January 2100. I'd be honoured if this code is still
        # being run 83 years from now!
        self.api.access_token_expiry = 4102444800
        self.assertTrue(
            self.api.token_valid()
        )

    def test_bearer_token_generator(self):
        # Generate a random token then check that the bearer string
        # is properly formed
        random_data = hexlify(os.urandom(30)).decode()
        self.api.access_token = random_data
        self.api.access_token_expiry = 4102444800
        self.assertEqual(
            self.api.get_bearer_token(),
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
                "active": True,
                "name": "test survey 1",
                "start_time": "10:00",
                "end_time": "12:00"
            }
        )
        pipeline.hmset(
            "occupeye:surveys:9992",
            {
                "id": 9992,
                "active": False,
                "name": "test survey 2",
                "start_time": "09:00",
                "end_time": "17:00"
            }
        )
        pipeline.expire("occupeye:surveys", 20)
        pipeline.expire("occupeye:surveys:9991", 20)
        pipeline.expire("occupeye:surveys:9992", 20)
        pipeline.execute()

        surveys = self.api.get_surveys()
        # When the data comes from the actual API it is backwards
        surveys.reverse()
        self.assertEqual(
            len(surveys),
            2
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
