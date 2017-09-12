from binascii import hexlify
from random import SystemRandom

import os
import textwrap


def generate_api_token():
    key = hexlify(os.urandom(30)).decode()
    dashes_key = ""
    for idx, char in enumerate(key):
        if idx % 15 == 0 and idx != len(key)-1:
            dashes_key += "-"
        else:
            dashes_key += char

    final = "uclapi" + dashes_key

    return final


def generate_temp_api_token():
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))
    final = "uclapi-temp-" + dashed

    return final


def generate_app_id():
    key = hexlify(os.urandom(5)).decode()
    final = "A" + key

    return final


def generate_app_client_id():
    sr = SystemRandom()

    client_id = '{}.{}'.format(
        ''.join(str(sr.randint(0, 9)) for _ in range(16)),
        ''.join(str(sr.randint(0, 9)) for _ in range(16))
    )

    return client_id


def generate_app_client_secret():
    client_secret = hexlify(os.urandom(32)).decode()
    return client_secret


def is_url_safe(url):
    protocols = os.environ["UCLAPI_CALLBACK_ALLOWED_PROTOCOLS"].split(';')
    denied_urls = os.environ["UCLAPI_CALLBACK_DENIED_URLS"].split(';')

    # If the URL does not start with a permitted protocol followed
    # by :// then deny it
    if not any([url.startswith(p + "://") for p in protocols]):
        return False

    # If the URL contains any of our denied URLs (such as uclapi.com)
    # then we deny it
    if any([(u in url) for u in denied_urls]):
        return False

    # Otherwise we assume all is ok and mark the URL as safe
    return True
