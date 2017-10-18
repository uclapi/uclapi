from binascii import hexlify
from random import SystemRandom

from common.helpers import generate_api_token

import os
import textwrap
import validators

def generate_temp_api_token():
    return generate_api_token("temp")


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
    if not url.startswith("https://"):
        return False

    if not validators.url(url, public=True):
        return False

    whitelist_urls = os.environ["WHITELISTED_CALLBACK_URLS"].split(';')
    if url in whitelist_urls:
        return True

    forbidden_urls = os.environ["FORBIDDEN_CALLBACK_URLS"].split(';')
    for furl in forbidden_urls:
        if furl in url:
            return False

    return True


def generate_secret():
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))

    return dashed
