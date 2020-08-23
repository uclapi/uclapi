from django.core.management.base import BaseCommand

from common.cachet import (
    get_incident_name,
    CachetException, create_incident
)
from workspaces.occupeye.cache import OccupeyeCache


class Command(BaseCommand):
    help = (
        'Caches current OccupEye sensor statuses into Redis'
    )

    def handle(self, *args, **options):
        try:
            print("Running Mini OccupEye Caching Operation")
            print("[+] Feeding Cache")
            cache = OccupeyeCache()
            cache.feed_cache(full=False)
            print("Done!")
            incident_name = get_incident_name("Occupeye-Mini")
            if incident_name:
                try:
                    create_incident("Occupeye mini cache succeeded",
                                    incident_name, 4)
                except CachetException as cachet_error:
                    print(f"Failed to create fixed cachet incident. "
                          f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    print(f"Unexpected: Failed to create fixed cachet "
                          f"incident. "
                          f"Reason: {repr(cachet_error)}")
            else:
                print("Could not find appropriate incident in Cachet!")
        except Exception as occupeye_error:
            incident_name = get_incident_name("Occupeye-Mini")
            if incident_name:
                try:
                    create_incident(occupeye_error, incident_name, 1)
                except CachetException as cachet_error:
                    print(f"Failed to create cachet incident. "
                          f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    print(f"Unexpected: Failed to create cachet incident. "
                          f"Reason: {repr(cachet_error)}")
            else:
                print("Could not find appropriate incident in Cachet!")
