from binascii import hexlify
from random import SystemRandom

from common.helpers import generate_api_token
from uclapi.settings import (
    MEDIUM_ARTICLE_QUANTITY,
    REDIS_UCLAPI_HOST,
    DEBUG
)
from django.core.management import call_command
import os
import redis
import textwrap
import validators


def get_articles():
    r = redis.Redis(host=REDIS_UCLAPI_HOST)
    if not r.exists("Blog:item:1:url"):
        if DEBUG:
            call_command('update_medium')
        else:
            return []
    pipe = r.pipeline()
    articles = []
    for i in range(0, MEDIUM_ARTICLE_QUANTITY):
        articles.append({})
        redis_key_url = "Blog:item:{}:url".format(i)
        redis_key_title = "Blog:item:{}:title".format(i)
        pipe.get(redis_key_url)
        pipe.get(redis_key_title)
    redis_response = pipe.execute()
    for i in range(0, MEDIUM_ARTICLE_QUANTITY):
        articles[i]['url'] = redis_response[i*2].decode("utf-8")
        articles[i]['title'] = redis_response[i*2+1].decode("utf-8")
    return articles


def generate_temp_api_token():
    return generate_api_token("temp")


def get_temp_token():
    r = redis.Redis(host=REDIS_UCLAPI_HOST)

    token = generate_temp_api_token()
    # We initialise a new temporary token and set it to 1
    # as it is generated at its first usage.
    r.set(token, 1, 600)
    return token


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


# Returns 0 if url is safe/valid
# Returns 1 if url doesn't start with https://
# Returns 2 if url is not valid format
# Returns 3 if url is in our blacklist
# Returns 4 if url is not public
def is_url_not_safe(url):
    if not url.startswith("https://"):
        return 1

    if not validators.url(url, public=True):
        if validators.url(url, public=False):
            return 4
        return 2

    whitelist_urls = os.environ["WHITELISTED_CALLBACK_URLS"].split(';')
    if url in whitelist_urls:
        return 0

    forbidden_urls = os.environ["FORBIDDEN_CALLBACK_URLS"].split(';')
    for furl in forbidden_urls:
        if furl in url:
            return 3

    return 0


def generate_secret():
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))

    return dashed
