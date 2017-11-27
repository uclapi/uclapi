import os
import redis
import requests

from django.conf import settings


class OccupEyeApi():
    """
    Python API for the Cad-Capture OccupEye backend.
    Data is cached as much as possible in Redis for performance.
    """
    def __init__(self):
        self.r = redis.StrictRedis(host=settings.REDIS_UCLAPI_HOST)
        self.deployment_id = os.environ["OCCUPEYE_DEPLOYMENT_ID"]
        self.deployment_name = os.environ["OCCUPEYE_DEPLOYMENT_NAME"]

    def get_deployments(self):
        pass