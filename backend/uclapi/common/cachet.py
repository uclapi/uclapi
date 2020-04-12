import cachetclient.cachet as cachet
import json
from django.conf import settings


class CachetException(Exception):
    pass


def get_incident_name(base):
    incident_name = None
    if settings.UCLAPI_DOMAIN_CURRENT == "staging.ninja":
        incident_name = base + "-Staging"
    elif settings.UCLAPI_DOMAIN_CURRENT == "uclapi.com":
        incident_name = base + "-Prod"
    return incident_name


def create_incident(error_message, component_name):
    components = cachet.Components(
        endpoint=settings.CACHET_URL, api_token=settings.CACHET_TOKEN)
    comp_list = json.loads(components.get())
    target_comp = None
    if "data" not in comp_list:
        raise CachetException("Failed to create cachet incident: "
                              "Failed to get list of components")
    for i in comp_list["data"]:
        if i["name"] == component_name:
            target_comp = i
            break
    if target_comp is None:
        raise CachetException("Failed to create cachet incident: "
                              "Cachet component not found!")
    if target_comp["status"] == 1:
        incidents = cachet.Incidents(
            endpoint=settings.CACHET_URL, api_token=settings.CACHET_TOKEN)
        message = f"Gencache failed on "
        f"{settings.UCLAPI_DOMAIN_CURRENT}"
        f" with error: {repr(error_message)}"
        incidents.post(
            name='Gencache failed',
            message=message,
            status=1,
            component_id=i["id"],
            component_status=4
        )


def delete_incident(component_name):
    components = cachet.Components(
        endpoint=settings.CACHET_URL, api_token=settings.CACHET_TOKEN)
    comp_list = json.loads(components.get())
    target_comp = None
    if "data" not in comp_list:
        raise CachetException("Failed to delete cachet incident: "
                              "Failed to get list of components")
    for i in comp_list["data"]:
        if i["name"] == component_name:
            target_comp = i
            break
    if target_comp is None:
        raise CachetException(
            "Failed to delete cachet incident: Cachet component not found!")
    if target_comp["status"] != 1:
        incidents = cachet.Incidents(
            endpoint=settings.CACHET_URL, api_token=settings.CACHET_TOKEN)
        inc_list = json.loads(incidents.get())
        for i in inc_list["data"]:
            if i["component_id"] == target_comp["id"]:
                incidents.put(
                    id=i["id"],
                    status=4,
                    component_id=target_comp["id"],
                    component_status=1
                )
                incidents.delete(id=i["id"])
