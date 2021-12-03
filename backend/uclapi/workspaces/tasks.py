from celery import shared_task
import requests
import os

from workspaces.occupeye.cache import OccupeyeCache
from workspaces.occupeye.endpoint import TestEndpoint


@shared_task
def feed_occupeye_cache(test=False, mini=False):
    print("Running OccupEye Caching Operation")
    print("[+] Feeding Cache")
    cache = OccupeyeCache(endpoint=TestEndpoint({})) if test else OccupeyeCache()
    cache.feed_cache(full=(not mini))


@shared_task
def day_cache():
    try:
        requests.get(os.environ.get("HEALTHCHECK_OCCUPEYE_DAY") + "/start", timeout=5)
    except requests.exceptions.RequestException:
        pass

    feed_occupeye_cache.s(mini=True)()

    try:
        requests.get(os.environ.get("HEALTHCHECK_OCCUPEYE_DAY"), timeout=5)
    except requests.exceptions.RequestException:
        pass


@shared_task
def night_cache():
    try:
        requests.get(os.environ.get("HEALTHCHECK_OCCUPEYE_NIGHT") + "/start", timeout=5)
    except requests.exceptions.RequestException:
        pass

    feed_occupeye_cache.s(mini=False)()

    try:
        requests.get(os.environ.get("HEALTHCHECK_OCCUPEYE_NIGHT"), timeout=5)
    except requests.exceptions.RequestException:
        pass
