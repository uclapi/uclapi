from abc import ABC, abstractmethod
from base64 import b64encode
from collections import defaultdict

import redis
import requests

from uclapi import settings
from workspaces.occupeye.constants import OccupEyeConstants
from .token import get_bearer_token


class Endpoint(ABC):
    @abstractmethod
    def request(self, url: str):
        pass

    @abstractmethod
    # Some results use fragmented JSON which is not supported by JSONDecode
    def request_fragment(self, url: str):
        pass

    @abstractmethod
    def image(self, image_id: int):
        pass


class OccupeyeEndpoint(Endpoint):
    def __init__(self):
        self._redis = redis.Redis(host=settings.REDIS_UCLAPI_HOST, charset="utf-8", decode_responses=True)
        self._const = OccupEyeConstants()

        access_token = self._redis.get(self._const.ACCESS_TOKEN_KEY)
        access_token_expiry = self._redis.get(self._const.ACCESS_TOKEN_EXPIRY_KEY)
        self.bearer_token = get_bearer_token(access_token, access_token_expiry, self._const)

    def request(self, url: str):
        headers = {"Authorization": self.bearer_token}
        r = requests.get(url=url, headers=headers)
        return r.json()

    def request_fragment(self, url: str):
        headers = {"Authorization": self.bearer_token}
        r = requests.get(url=url, headers=headers)
        return r.text.replace("\"", "")

    def image(self, image_id: int):
        headers = {"Authorization": self.bearer_token}
        url = self._const.URL_IMAGE.format(image_id)
        response = requests.get(url=url, headers=headers, stream=True)
        content_type = response.headers["Content-Type"]

        raw_image = response.content
        image_b64 = b64encode(raw_image)
        return image_b64, content_type


class TestEndpoint(Endpoint):
    def __init__(self, responses: dict):
        self._const = OccupEyeConstants()
        self._results = defaultdict(dict, responses)

    def request(self, url: str):
        print("Requesting: %s" % url)
        return self._results[url]

    def request_fragment(self, url: str):
        print("Requesting fragment: %s" % url)
        return self._results[url]

    def image(self, image_id: int):
        url = self._const.URL_IMAGE.format(image_id)
        print("Requesting image: %s" % url)
        entry = self._results[url]
        if "image" not in entry or "content_type" not in entry:
            return "", ""
        return entry["image"], entry["content_type"]
