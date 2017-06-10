from binascii import hexlify
import os
import textwrap


def generate_user_token():
    key = hexlify(os.urandom(30)).decode()
    dashes_key = ""
    '-'.join(textwrap.wrap(key, 15))

    final = "uclapi-user" + dashes_key

    return final


def generate_random_verification_code():
    key = hexlify(os.urandom(40)).decode()
    final = "verify" + key
    return final
