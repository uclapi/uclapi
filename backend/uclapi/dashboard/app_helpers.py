from binascii import hexlify
from random import SystemRandom

import os
import string


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


def generate_app_id():
    key = hexlify(os.urandom(5)).decode()
    final = "A" + key

    return final


def generate_app_client_id():
    sr = SystemRandom()

    client_id = ''.join(str(sr.randint(0, 9)) for _ in range(16))
    client_id += "."
    client_id += ''.join(str(sr.randint(0, 9)) for _ in range(16))

    return client_id


def generate_app_client_secret():
    client_secret = hexlify(os.urandom(32)).decode()
    return client_secret
