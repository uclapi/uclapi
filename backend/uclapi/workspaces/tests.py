import os
from binascii import hexlify

import redis

from django.conf import settings
from django.test import TestCase

from .occupeye import OccupEyeApi

class OccupEyeApiTestCase(TestCase):
    def setUp(self):
        self.r = redis.StrictRedis(
            host=settings.REDIS_UCLAPI_HOST
        )

        # Ensure we have no tokens in Redis yet
        self.r.delete("OCCUPEYE_ACCESS_TOKEN")
        self.r.delete("OCCUPEYE_ACCESS_TOKEN_EXPIRY")

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
