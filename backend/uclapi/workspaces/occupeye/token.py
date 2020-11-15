import json
from time import time as time_now

import requests


def get_token(consts):
    """
    Gets a fresh OAuth 2.0 Bearer token based on the
    username and password stored in the environment.
    """
    url = consts.BASE_URL + "/token"
    body = {
        "Grant_type": "password",
        "Username": consts.USERNAME,
        "Password": consts.PASSWORD,
    }

    response = requests.post(url=url, data=body)

    response_data = json.loads(response.text)

    access_token = response_data["access_token"]
    access_token_expiry = int(time_now()) + int(response_data["expires_in"])

    return (access_token, access_token_expiry)


def token_valid(access_token, access_token_expiry):
    """
    Checks if the token exists and has not expired.
    """
    if not access_token:
        return False

    if not access_token_expiry:
        return False

    # Ensure the access token has not expired since we last checked
    if time_now() > int(access_token_expiry):
        return False

    return True


def get_bearer_token(access_token, access_token_expiry, consts):
    """
    If a token is valid, it returns the Bearer string
    used in the Authorization header.
    """
    if not token_valid(access_token, access_token_expiry):
        (access_token, _) = get_token(consts)

    return "Bearer " + access_token
