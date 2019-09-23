"""
WSGI config for uclapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

import eventlet

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from common.helpers import read_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

read_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uclapi.settings")

# Patch the socket libraries to work properly
# This is crucial for multiprocessing to work
# We only do this if the environment variable
# to not patch doesn't exist.
# This is because the patch breaks runserver.
if os.environ.get("EVENTLET_NOPATCH") != 'True':
    eventlet.monkey_patch()

application = get_wsgi_application()
