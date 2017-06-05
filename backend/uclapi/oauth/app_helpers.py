from binascii import hexlify
import os


def generate_user_token():
    key = hexlify(os.urandom(30)).decode()
    dashes_key = ""
    for idx, char in enumerate(key):
        if idx % 15 == 0 and idx != len(key)-1:
            dashes_key += "-"
        else:
            dashes_key += char

    final = "uclapi-user" + dashes_key

    return final


def generate_random_verification_code():
    key = hexlify(os.urandom(40)).decode()
    final = "verify" + key
    return final
