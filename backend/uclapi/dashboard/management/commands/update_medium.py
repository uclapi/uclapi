from django.core.management.base import BaseCommand
from django.conf import settings
import redis
import xml.etree.ElementTree as ET
from requests import get as rget


class Command(BaseCommand):

    help = 'Surveys medium blogs on website'

    def handle(self, *args, **options):
        print("Getting latest medium articles")
        response = rget(url="https://medium.com/feed/ucl-api")
        root = ET.fromstring(response.text)
        medium_article_iterator = root.iter('item')

        print("Connecting to Redis")
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        pipe = self._redis.pipeline()
        print("Setting Blog keys")
        for i in range(0, settings.MEDIUM_ARTICLE_QUANTITY):
            article = next(medium_article_iterator)
            redis_key_title = "Blog:item:{}:title".format(i)
            redis_key_url = "Blog:item:{}:url".format(i)
            redis_key_tags = "Blog:item:{}:tags".format(i)
            redis_key_creator = "Blog:item:{}:creator".format(i)
            redis_key_published = "Blog:item:{}:published".format(i)
            redis_key_updated = "Blog:item:{}:updated".format(i)
            redis_key_content = "Blog:item:{}:content".format(i)
            redis_key_image_url = "Blog:item:{}:image_url".format(i)

            title = article[0].text
            url = article[1].text
            # short_link = article[2].text
            tags = article[3].text
            index = 4
            while article[index].tag == "category":
                tags += ", " + article[index].text
                index += 1

            creator = article[index].text
            published = article[index + 1].text
            updated = article[index + 2].text

            content = article[index + 3].text
            link = 'url_not_found'

            if content.startswith("<figure><img"):
                link = content[25:]
                split = link.split('" />')
                link = split[0]

            pipe.set(redis_key_title, title)
            pipe.set(redis_key_url, url)
            pipe.set(redis_key_tags, tags)
            pipe.set(redis_key_creator, creator)
            pipe.set(redis_key_published, published)
            pipe.set(redis_key_updated, updated)
            pipe.set(redis_key_content, content)
            pipe.set(redis_key_image_url, link)

        pipe.execute()
        print("Frontend updated to have latest medium blogs")
