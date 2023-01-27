import os
import logging

import requests
from celery import shared_task

from workspaces.occupeye.archive import OccupEyeArchive
from workspaces.occupeye.cache import OccupeyeCache
from workspaces.occupeye.endpoint import TestEndpoint


@shared_task
def feed_occupeye_cache(test=False, mini=False):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("Running OccupEye Caching Operation")
    logging.info("[+] Feeding Cache")
    cache = OccupeyeCache(endpoint=TestEndpoint({})) if test else OccupeyeCache()
    cache.feed_cache(full=(not mini))


@shared_task
def feed_occupeye_archive(test=False, delete=False):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info("Running OccupEye Archive Operation")
    logging.info("[+] Fetching Archive")
    archive = OccupEyeArchive(endpoint=TestEndpoint({})) if test else OccupEyeArchive()
    if delete:
        archive.reset()
    archive.update()


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
    feed_occupeye_archive()

    try:
        requests.get(os.environ.get("HEALTHCHECK_OCCUPEYE_NIGHT"), timeout=5)
    except requests.exceptions.RequestException:
        pass
