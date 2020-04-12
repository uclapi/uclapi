from django.core.management.base import BaseCommand

from common.cachet import create_incident, CachetException, delete_incident, \
    get_incident_name
from workspaces.occupeye.cache import OccupeyeCache


class Command(BaseCommand):
    help = (
        'Caches all OccupEye data into Redis including historical data'
    )

    def handle(self, *args, **options):
        try:
            print("Running OccupEye Caching Operation")
            print("[+] Feeding Cache")
            cache = OccupeyeCache()
            cache.feed_cache(full=True)
            print("Done!")
            incident_name = get_incident_name("Occupeye")
            if incident_name is not None:
                delete_incident(incident_name)
        except Exception as occupeye_error:
            incident_name = get_incident_name("Occupeye")
            if incident_name is not None:
                try:
                    create_incident(occupeye_error, incident_name)
                except CachetException as cachet_error:
                    print(f"Failed to create cachet incident. "
                          f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    print(f"Unexpected: Failed to create cachet incident. "
                          f"Reason: {repr(cachet_error)}")
