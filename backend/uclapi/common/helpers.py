import os
import textwrap

from binascii import hexlify

from django.http import JsonResponse
from dotenv import read_dotenv as rd 

def read_dotenv(path = None):
    if not os.environ.get('DOCKER') == "yes":
        rd(path)

class PrettyJsonResponse(JsonResponse):
    def __init__(self, data, rate_limiting_data=None):
        # Calls JsonResponse's constructure and requests 4 line indenting
        super().__init__(data, json_dumps_params={'indent': 4})

        # Adds rate limiting headers from a passed view kwargs
        rate_limit_headers = {
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Retry-After'
        }
        if rate_limiting_data:
            for header in rate_limit_headers:
                if header in rate_limiting_data:
                    self[header] = rate_limiting_data[header]


def generate_api_token(prefix=None):
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))

    if prefix:
        final = "uclapi-{}-{}".format(prefix, dashed)
    else:
        final = "uclapi-" + dashed

    return final
