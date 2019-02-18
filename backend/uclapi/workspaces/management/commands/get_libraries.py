import re
import redis
import requests

from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from lxml import etree

class Command(BaseCommand):
    help = 'Caches each Library into Redis with the opening hours'

    def get_current_term(self):
        # Generate a Term Dates URL from the Set ID, e.g. LIVE-18-19
        split_set_id = settings.ROOMBOOKINGS_SETID.split('-')

        # Expected year string: 2019-20
        year_string = "20{}-{}".format(split_set_id[1], split_set_id[2])

        term_dates_base_url = \
            "https://www.ucl.ac.uk/students/life-ucl/term-dates-and-closures/term-dates-and-closures"  # noqa

        term_dates_url = "{}-{}".format(term_dates_base_url, year_string)
        r = requests.get(term_dates_url)
        term_table = '<data>' + r.text.split(
            '<table border="1" cellpadding="1" cellspacing="1">'
        )[1].split('</table>')[0] + '</data>'
        parser = etree.XMLParser(target=etree.TreeBuilder())
        root = etree.XML(term_table, parser)
        # term_1_start = root.find("./tbody/tr[1]/td[2]").text.split(' to ')[0]
        term_2_start = root.find("./tbody/tr[2]/td[2]").text.split(' to ')[0]
        term_3_start = root.find("./tbody/tr[3]/td[2]").text.split(' to ')[0]

        date_format = '%A %d %B %Y'

        # term_1_date = datetime.strptime(term_1_start, date_format).date()
        term_2_date = datetime.strptime(term_2_start, date_format).date()
        term_3_date = datetime.strptime(term_3_start, date_format).date()

        date_today = datetime.now().date()

        # We need to investigate how this will work in the summer
        # e.g. if we switch to LIVE-19-20 but the current summer is
        # LIVE-18-19
        if date_today >= term_3_date:
            return 3
        elif date_today >= term_2_date:
            return 2
        else:
            return 1

    def get_library_hours(self, term_number):
        pass

    def handle(self, *args, **options):
        current_term = self.get_current_term()
        print("Currently using {}, we are in Term {}".format(
            settings.ROOMBOOKINGS_SETID,
            current_term
        ))

        library_hours = self.get_library_hours(current_term)
