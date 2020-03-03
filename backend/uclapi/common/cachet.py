import cachetclient.cachet as cachet
import json
from django.conf import settings

ENDPOINT = settings.CACHET_URL
API_TOKEN = settings.CACHET_TOKEN

def create_incident(error_message, component_name):
    try:
        components = cachet.Components(endpoint=ENDPOINT, api_token=API_TOKEN)
        comp_list = json.loads(components.get())
        target_comp = None
        for i in comp_list["data"]:
            if i["name"] == component_name:
                target_comp = i
                break
        if target_comp["status"] == 1:
            incidents = cachet.Incidents(endpoint=ENDPOINT, api_token=API_TOKEN)
            message = f"Gencache failed on "
                      f"{settings.UCLAPI_DOMAIN_CURRENT}"
                      f" with error: {repr(error_message)}"
            new_incident = json.loads(incidents.post(name='Gencache failed',
                                 message=message,
                                 status=1,
                                 component_id=i["id"],
                                 component_status=4))

    except Exception as cachet_error:
        print(f"Failed to create cachet incident. "
              f"Reason: {repr(cachet_error)}")

def delete_incident(component_name):
    try:
        components = cachet.Components(endpoint=ENDPOINT, api_token=API_TOKEN)
        comp_list = json.loads(components.get())
        target_comp = None
        for i in comp_list["data"]:
            if i["name"] == component_name:
                target_comp = i
                break
        if target_comp["status"] != 1:
            incidents = cachet.Incidents(endpoint=ENDPOINT, api_token=API_TOKEN)
            inc_list = json.loads(incidents.get())
            for i in inc_list["data"]:
                if i["component_id"] == target_comp["id"]:
                    incidents.put(id=i["id"], status=4, component_id=target_comp["id"], component_status=1)
                    incidents.delete(id=i["id"])

    except Exception as cachet_error:
        print(f"Failed to create cachet incident. "
              f"Reason: {repr(cachet_error)}")
