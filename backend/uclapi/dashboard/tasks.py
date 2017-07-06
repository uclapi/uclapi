from __future__ import absolute_import
import keen

from celery import shared_task


@shared_task
def test_task(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def keen_add_event_task(title, data):
    try:
        keen.add_event(title, data)
    except Exception:
        return 'Keen failed for event titled ' + \
                title + 'Please check your internet connection.'

    return 'Keen added a new event titled ' + title
