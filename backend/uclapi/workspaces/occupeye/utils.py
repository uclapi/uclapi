import requests

from .exceptions import BadOccupEyeRequest


def str2bool(v):
    """
    Converts a string representation of a boolean
    into an actual boolean object. This is used
    to convert the boolean strings from Redis into
    actual bool objects.
    """
    return str(v).lower() in ("yes", "true", "t", "1")


def authenticated_request(url, bearer):
    headers = {
        "Authorization": bearer
    }
    r = requests.get(
        url=url,
        headers=headers
    )
    return r.json()


def chunk_list(l, chunk_size):
        """
        Splits a list into even chunks.
        https://stackoverflow.com/a/312464/5297057
        """
        for i in range(0, len(l), chunk_size):
            yield l[i:i+chunk_size]


def survey_ids_to_surveys(surveys_data, survey_ids):
        if survey_ids:
            try:
                survey_ids_list = [int(x) for x in survey_ids.split(',')]
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
