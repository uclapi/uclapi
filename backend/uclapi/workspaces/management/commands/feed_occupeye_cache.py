from django.core.management.base import BaseCommand

from workspaces.occupeye.cache import OccupeyeCache


class Command(BaseCommand):
    help = (
        'Caches historical OccupEye data into redis'
    )

    def handle(self, *args, **options):
        print("Running OccupEye Caching Operation")
        print("[+] Feeding Cache")
        cache = OccupeyeCache()
        cache.feed_cache(full=True)
        print("Done!")
