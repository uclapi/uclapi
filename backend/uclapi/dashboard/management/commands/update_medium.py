from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from requests import get as rget

class Command(BaseCommand):

    help = 'Updates medium blogs on website'

    def handle(self, *args, **options):
        print("Getting latest medium articles")
        response = rget(url="https://medium.com/feed/ucl-api")
        root = ET.fromstring(response.text)
        file_data = []
        print("Editing Blog.jsx")
        with open("../../frontend/src/components/getStarted/Blog.jsx", "r") as f:
            for line in f:
                file_data.append(line)
        medium_article_iterator = root.iter('item')
        for i in range(0, len(file_data)):
            if file_data[i].strip()[0:3] == "<a ":
                article = next(medium_article_iterator)
                for j in range(0, len(file_data[i])):
                    if file_data[i][j] != " ":
                        buffer = j
                        break
                file_data[i] = buffer*" " + "<a href=\""+article[1].text+"\">\n"
                for j in range(0, len(file_data[i+1])):
                    if file_data[i+1][j] != " ":
                        buffer = j
                        break
                file_data[i+1] = buffer*" " + article[0].text + "\n"

        with open("../../frontend/src/components/getStarted/Blog.jsx", "w") as f:
            for line in file_data:
                f.write(line)
        print("Frontend updated to have latest medium blogs")
