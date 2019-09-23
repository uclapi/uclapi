import datetime
import os
import textwrap

from binascii import hexlify

from django.http import JsonResponse, HttpResponse

from dotenv import read_dotenv as rd


def read_dotenv(path=None):
    if not os.environ.get('DOCKER') == "yes":
        rd(path)


LOCAL_TIMEZONE = (
    datetime.datetime.now(datetime.timezone.utc)
    .astimezone()
    .tzinfo
)


CUSTOM_HEADERS = [
    'Last-Modified',
    'X-RateLimit-Limit',
    'X-RateLimit-Remaining',
    'X-RateLimit-Retry-After'
]


class PrettyJsonResponse(JsonResponse):
    def __init__(self, data, custom_header_data=None):
        # Calls JsonResponse's constructure and requests 4 line indenting
        super().__init__(data, json_dumps_params={'indent': 4})

        # Adds custom headers from a passed view kwargs
        if custom_header_data:
            for header in CUSTOM_HEADERS:
                if header in custom_header_data:
                    self[header] = custom_header_data[header]


class RateLimitHttpResponse(HttpResponse):
    def __init__(self, content=b'', custom_header_data=None, *args, **kwargs):
        super().__init__(content, *args, **kwargs)

        # Adds custom headers from a passed view kwargs
        if custom_header_data:
            for header in CUSTOM_HEADERS:
                if header in custom_header_data:
                    self[header] = custom_header_data[header]


def generate_api_token(prefix=None):
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))

    if prefix:
        final = "uclapi-{}-{}".format(prefix, dashed)
    else:
        final = "uclapi-" + dashed

    return final
