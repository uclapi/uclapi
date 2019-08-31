from __future__ import absolute_import

import os
import requests

from celery import shared_task


@shared_task
def test_task(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def add_user_to_mailing_list_task(email, name):
    add_user_to_mailing_list(email, name)


def add_user_to_mailing_list(email, name):
    data = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "EMAIL": email,
            "FNAME": name
        }
    }

    headers = {
        "Authorization": "apikey {}".format(
            os.environ["MAILCHIMP_API_KEY"])
    }

    requests.post(
        os.environ["MAILCHIMP_ENDPOINT"], json=data, headers=headers)
