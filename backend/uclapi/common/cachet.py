import cachetclient
from cachetclient.v1 import enums
from django.conf import settings

"""
This file handles all things cachet. From creating incidents to deleting
them when fixed. The results can be seen on our cachet status dashboard at
https://cachet.apps.uclapi.com/ .

Incidents can be added to components of which we currently have 8 indicating
problems with that specific system.
List of components and their ID's:
Gencache-Staging 1,
Occupeye-Staging 3,
Occupeye-Mini-Staging 6,
OAuth-Staging 7,
Gencache-Prod 2,
Occupeye-Prod 4,
Occupeye-Mini-Prod 5,
OAuth-Prod 8

You can add a component in the admin dashboard and then reference it using
the functions in this file without finding out its ID or attached information.

More documentation on cachet endpoints can be found at
https://docs.cachethq.io/reference
and general documentation at
https://docs.cachethq.io/docs
"""


class CachetException(Exception):
    pass


def get_incident_name(base: str) -> str:
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


def create_incident(error_message: str, component_name: str,
                    incident_status: int, comp_status: int):
    """
    Create an incident with the error message and status specified for the
    component with its name and new status specified. The status is specified
    by the
    cachet.enums enum. Only creates an incident if the component isn't
    already down.

    :param error_message: Error message to display on incident
    :type error_message: str
    :param component_name: Component name to create incident for
    :type component_name: str
    :param incident_status: Status for the incident
    :type incident_status: int
    :param comp_status: Status for the component
    :type comp_status: int
    """

    cachet_client = cachetclient.Client(endpoint=settings.CACHET_URL,
                                        api_token=settings.CACHET_TOKEN,
                                        version="1")

    target_comp = _get_component(cachet_client, component_name)

    if target_comp.status == enums.COMPONENT_STATUS_OPERATIONAL:

        message = (f"{component_name} failed on "
                   f"{settings.UCLAPI_DOMAIN_CURRENT}"
                   f" with error: {repr(error_message)}")

        cachet_client.incidents.create(
            name=f"{component_name} failed",
            message=message,
            status=incident_status,
            component_id=target_comp.id,
            component_status=comp_status
        )


def update_incident(update_message: str, component_name: str,
                    status: int):
    """
    Update an incident with the update message and status specified for the
    component with its name specified . The status is specified by the
    cachet.enums enum. Only updates if the component is down.

    :param update_message: Update message to display on incident
    :type update_message: str
    :param component_name: Component name to create incident for
    :type component_name: str
    :param status: Status for the incident
    :type status: int
    """

    cachet_client = cachetclient.Client(endpoint=settings.CACHET_URL,
                                        api_token=settings.CACHET_TOKEN,
                                        version="1")

    target_comp = _get_component(cachet_client, component_name)

    target_incident = _get_incident(cachet_client, target_comp)

    if target_comp.status != enums.COMPONENT_STATUS_OPERATIONAL:
        cachet_client.incident_updates.create(
            incident_id=target_incident.id,
            status=status,
            message=update_message
        )

        if status == enums.INCIDENT_FIXED:
            target_comp.status = enums.COMPONENT_STATUS_OPERATIONAL
            target_comp.update()


def _get_component(client: cachetclient.v1.Client, comp_name: str) -> \
        cachetclient.v1.components.Component:
    """
    Given a component name returns the actual component object.

    :param client: cachet client instance
    :type client: cachetclient.v1.Client
    :param comp_name: Component name to fetch
    :type comp_name: str
    :return: Component object with the given name
    :rtype: cachetclient.v1.components.Component
    """

    for i in client.components.list():
        if i.name == comp_name:
            return i

    # If we fail to find it raise an error

    raise CachetException(
        "Failed to get cachet incident: Cachet component not found!"
    )


def _get_incident(cachet_client: cachetclient.v1.Client, target_comp:
                  cachetclient.v1.components.Component) -> \
        cachetclient.v1.incidents.Incident:
    """

    :param cachet_client: cachet client instance
    :type cachet_client: cachetclient.v1.Client
    :param target_comp: Component to get incident from
    :type target_comp: cachetclient.v1.components.Component
    :return: Incident to update
    :rtype: cachetclient.v1.incidents.Incident
    """

    incidents = cachet_client.incidents.list()
    for i in incidents:
        if i.component_id == target_comp.id and i.status != \
                enums.INCIDENT_FIXED:
            return i

    raise CachetException("Failed to get cachet incident: Cachet Incident not "
                          "found!")
