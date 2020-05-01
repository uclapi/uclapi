import cachetclient.cachet as cachet
import json
from django.conf import settings

"""
This file handles all things cachet. From creating incidents to deleting
them when fixed. The results can be seen on our cachet status dashboard at
https://cachet.apps.uclapi.com/ .

Incidents can be added to components of which we currently have 6 indicating
problems with that specific system.
List of components:
Gencache-Staging,
Occupeye-Staging,
Occupeye-Mini-Staging,
Gencache-Prod,
Occupeye-Prod,
Occupeye-Mini-Prod

You can add a component in the admin dashboard and then reference it using
the functions in this file without finding out its ID or attached information.

More documentation on cachet endpoints can be found at
https://docs.cachethq.io/reference
and general documentation at
https://docs.cachethq.io/docs
"""


class CachetException(Exception):
    pass


def get_incident_name(base):
    """
    Get and append the appropriate suffix for the component using the current
    domain. For example if we are running on staging.ninja we add the
    '-staging' suffix.

    :param base: Base incident name
    :type base: str
    :return: Base incident name with correct environment suffix such as
    -prod or -staging
    :rtype: str

    """

    incident_name = ""

    if settings.UCLAPI_DOMAIN_CURRENT == "staging.ninja":
        incident_name = base + "-Staging"
    elif settings.UCLAPI_DOMAIN_CURRENT == "uclapi.com":
        incident_name = base + "-Prod"

    return incident_name


def create_incident(error_message, component_name):
    """
    Create an incident with the error message specified for the component
    name specified. This marks the status as 4 - major outage - and the
    incident status as 1 - investigating.

    :param error_message: Error message to display on incident
    :type error_message: str
    :param component_name: Component name to create incident for
    :type component_name: str
    """

    target_comp = _get_component(component_name)

    # If component is not already in an outage, create an incident and
    # change the components status
    if target_comp["status"] == 1:
        incidents = cachet.Incidents(
            endpoint=settings.CACHET_URL,
            api_token=settings.CACHET_TOKEN
        )
        message = (f"Gencache failed on "
                   f"{settings.UCLAPI_DOMAIN_CURRENT}"
                   f" with error: {repr(error_message)}")
        incidents.post(
            name='Gencache failed',
            message=message,
            status=1,
            component_id=target_comp["id"],
            component_status=4
        )


def delete_incident(component_name):
    """
    Deletes the incident associated with the component given by name. This
    changes the component status to 1 - operational - and then deletes the
    incident.

    :param component_name: Component name to delete incident for
    :type component_name: str
    """

    target_comp = _get_component(component_name)

    # If component is not operational, then delete the incident and update
    # the components status.
    if target_comp["status"] != 1:
        incidents = cachet.Incidents(
            endpoint=settings.CACHET_URL,
            api_token=settings.CACHET_TOKEN
        )
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


def _get_component(comp_name):
    """
    Given a component name returns the actual component object.

    :param comp_name: Component name to fetch
    :type comp_name: str
    :return: Component object with the given name
    :rtype: dict
    """

    components = cachet.Components(
        endpoint=settings.CACHET_URL,
        api_token=settings.CACHET_TOKEN
    )
    comp_list = json.loads(components.get())
    target_comp = None
    if "data" not in comp_list:
        raise CachetException("Failed to get cachet incident: "
                              "Failed to get list of components")

    for i in comp_list["data"]:
        if i["name"] == comp_name:
            target_comp = i
            break

    if target_comp is None:
        raise CachetException(
            "Failed to get cachet incident: Cachet component not found!"
        )
    return target_comp
