from django.core.management.base import BaseCommand

from workspaces.occupeye.cache import OccupeyeCache


class Command(BaseCommand):
    help = (
        'Caches all OccupEye data into Redis including historical data'
    )

    def handle(self, *args, **options):
        print("Running OccupEye Caching Operation")
        print("[+] Feeding Cache")
        cache = OccupeyeCache()
        cache.feed_cache(full=True)
        print("Done!")
