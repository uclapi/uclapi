import datetime
import requests

from dateutil import parser as dateutil_parser
from pytz import timezone

from .exceptions import BadOccupEyeRequest, OccupEyeOtherSensorState


def authenticated_request(url, bearer):
    headers = {
        "Authorization": bearer
    }
    r = requests.get(
        url=url,
        headers=headers
    )
    return r.json()


def survey_ids_to_surveys(surveys_data, survey_ids):
        if survey_ids:
            try:
                # If we use a set instead of a list then we drop duplicates.
                # This avoids the user specifying a filter with a bad
                # ID and a duplicate good one, which would cause issues.
                survey_ids_list = {int(x) for x in survey_ids.split(',')}
            except ValueError:
                raise BadOccupEyeRequest
        else:
            survey_ids_list = None

        filtered_surveys = []

        if survey_ids_list:
            for survey in surveys_data:
                if survey["id"] in survey_ids_list:
                    filtered_surveys.append(survey)
        else:
            filtered_surveys = surveys_data

        if survey_ids_list:
            if len(filtered_surveys) != len(survey_ids_list):
                raise BadOccupEyeRequest

        return filtered_surveys


def is_sensor_occupied(last_trigger_type, last_trigger_timestamp):
    if last_trigger_type == "Occupied":
        return True

    # If the seat is neither occupied nor absent, consider
    # it other and raise an exception to handle this event
    if last_trigger_type != "Absent":
        raise OccupEyeOtherSensorState

    # At this point the sensor is marked as Absent
    # Remove 30 minutes from the trigger time to account for
    # UCL's 30 minute library seat absence policy
    # https://www.ucl.ac.uk/library/articles/2017/study-space-main-science

    # Convert the ISO8601 timestamp to a datetime object we can work with
    trigger_time = dateutil_parser.parse(
        last_trigger_timestamp
    )
    # Get the local time 30 minutes ago
    london = timezone('Europe/London')
    minimum_time = datetime.datetime.now(tz=london) - \
        datetime.timedelta(minutes=30)

    # If the sensor was marked absent at least 30 minutes ago
    # then we consider it to be absent. Otherwise we consider it
    # to be occupied.
    if trigger_time <= minimum_time:
        return False

    # The sensor was marked absent, but not recently enough.
    # Therefore, we consider that seat to be occupied
    return True
