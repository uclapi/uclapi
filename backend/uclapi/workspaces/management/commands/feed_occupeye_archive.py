import logging
import sys
import traceback

from cachetclient.v1 import enums
from django.core.management.base import BaseCommand

from common.cachet import (
    create_incident,
    CachetException,
    get_incident_name,
    update_incident,
)
from workspaces.occupeye.archive import OccupEyeArchive
from workspaces.occupeye.endpoint import TestEndpoint


class Command(BaseCommand):
    help = "Surveys new historical OccupEye data in Postgres"

    def add_arguments(self, parser):
        parser.add_argument("--test", action='store_true')
        parser.add_argument("--full", action='store_true')

    def handle(self, *args, **options):
        try:
            logging.basicConfig(level=logging.INFO)
            logging.info("Running OccupEye Archive Operation")
            logging.info("[+] Feeding Archive")
            if options['test']:
                archive = OccupEyeArchive(endpoint=TestEndpoint({}))
            else:
                archive = OccupEyeArchive()
            if options['full']:
                archive.reset()
            archive.update()
            logging.info("[+] Done!")
            incident_name = get_incident_name("Occupeye")
            if incident_name:
                try:
                    update_incident("Occupeye Archive succeeded", incident_name, enums.INCIDENT_FIXED)
                except CachetException as cachet_error:
                    logging.error(f"Failed to create fixed cachet incident. " f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    logging.error(
                        f"Unexpected: Failed to create fixed cachet " f"incident. " f"Reason: {repr(cachet_error)}")
            else:
                logging.error("No incident present in Cachet!")
        except Exception as occupeye_error:
            incident_name = get_incident_name("Occupeye-Archive")
            if incident_name:
                try:
                    create_incident(
                        str(occupeye_error),
                        incident_name,
                        enums.INCIDENT_INVESTIGATING,
                        enums.COMPONENT_STATUS_MAJOR_OUTAGE,
                    )
                except CachetException as cachet_error:
                    logging.error(f"Failed to create cachet incident. " f"Reason: {repr(cachet_error)}")
                except Exception as cachet_error:
                    logging.error(f"Unexpected: Failed to create cachet incident. " f"Reason: {repr(cachet_error)}")
            else:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                logging.error("Could not find appropriate incident in Cachet!")
