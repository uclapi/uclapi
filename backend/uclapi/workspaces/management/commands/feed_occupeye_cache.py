from django.core.management.base import BaseCommand

from workspaces.occupeye import OccupEyeApi


class Command(BaseCommand):
    help = (
        'Feeds the OccupEye data into Redis so that response times are quicker'
    )

    def handle(self, *args, **options):
        print("Running OccupEye Caching Operation")
        print("[+] Getting Key")
        api = OccupEyeApi()
        api.get_token()
        print("[+] Feeding Cache")
        api.feed_cache()
        print("Done!")
