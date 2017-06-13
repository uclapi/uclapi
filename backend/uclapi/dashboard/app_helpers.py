import os
from binascii import hexlify


def generate_api_token(temp=False):
    key = hexlify(os.urandom(30)).decode()
    dashes_key = ""
    for idx, char in enumerate(key):
        if idx % 15 == 0 and idx != len(key)-1:
            dashes_key += "-"
        else:
            dashes_key += char

    final = "uclapi" + dashes_key

    return final


def generate_temp_api_token(temp=False):
    key = hexlify(os.urandom(30)).decode()
    dashes_key = ""
    for idx, char in enumerate(key):
        if idx % 15 == 0 and idx != len(key)-1:
            dashes_key += "-"
        else:
            dashes_key += char

    final = "uclapi-temp" + dashes_key

    return final


def generate_app_id():
    key = hexlify(os.urandom(5)).decode()
    final = "A" + key

    return final
