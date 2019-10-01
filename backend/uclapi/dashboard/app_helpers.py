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

NOT_HTTPS = 1
NOT_VALID = 2
URL_BLACKLISTED = 3
NOT_PUBLIC = 4


def get_articles():
    r = redis.Redis(host=REDIS_UCLAPI_HOST)
    if not r.exists("Blog:item:1:updated"):
        if DEBUG:
            call_command('update_medium')
        else:
            return []
    pipe = r.pipeline()
    articles = []
    for i in range(0, MEDIUM_ARTICLE_QUANTITY):
        articles.append({})

        redis_key_title = "Blog:item:{}:title".format(i)
        redis_key_url = "Blog:item:{}:url".format(i)
        redis_key_tags = "Blog:item:{}:tags".format(i)
        redis_key_creator = "Blog:item:{}:creator".format(i)
        redis_key_published = "Blog:item:{}:published".format(i)
        redis_key_updated = "Blog:item:{}:updated".format(i)
        redis_key_content = "Blog:item:{}:content".format(i)
        redis_key_image_url = "Blog:item:{}:image_url".format(i)

        pipe.get(redis_key_title)
        pipe.get(redis_key_url)
        pipe.get(redis_key_tags)
        pipe.get(redis_key_creator)
        pipe.get(redis_key_published)
        pipe.get(redis_key_updated)
        pipe.get(redis_key_content)
        pipe.get(redis_key_image_url)

    redis_response = pipe.execute()
    for i in range(0, MEDIUM_ARTICLE_QUANTITY):
        start_index = i*8
        type = "utf-8"

        articles[i]['title'] = redis_response[start_index].decode(type)
        articles[i]['url'] = redis_response[start_index+1].decode(type)
        articles[i]['tags'] = redis_response[start_index+2].decode(type)
        articles[i]['creator'] = redis_response[start_index+3].decode(type)
        articles[i]['published'] = redis_response[start_index+4].decode(type)
        articles[i]['updated'] = redis_response[start_index+5].decode(type)
        articles[i]['content'] = redis_response[start_index+6].decode(type)
        articles[i]['image_url'] = redis_response[start_index+7].decode(type)
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


def is_url_unsafe(url):
    if not url.startswith("https://"):
        return NOT_HTTPS

    if not validators.url(url, public=True):
        if validators.url(url, public=False):
            return NOT_PUBLIC
        return NOT_VALID

    whitelist_urls = os.environ["WHITELISTED_CALLBACK_URLS"].split(';')
    if url in whitelist_urls:
        return 0

    forbidden_urls = os.environ["FORBIDDEN_CALLBACK_URLS"].split(';')
    for furl in forbidden_urls:
        if furl in url:
            return URL_BLACKLISTED

    return 0


def generate_secret():
    key = hexlify(os.urandom(30)).decode()
    dashed = '-'.join(textwrap.wrap(key, 15))

    return dashed
