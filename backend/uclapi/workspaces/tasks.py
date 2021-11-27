from celery import shared_task

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
    feed_occupeye_cache.s(mini=True)()


@shared_task
def night_cache():
    feed_occupeye_cache.s(mini=False)()
