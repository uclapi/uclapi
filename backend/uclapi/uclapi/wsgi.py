"""
WSGI config for uclapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import urllib.request
import shutil

import eventlet

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from common.helpers import read_dotenv

read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uclapi.settings")

# Patch the socket libraries to work properly
# This is crucial for multiprocessing to work
# We only do this if the environment variable
# to not patch doesn't exist.
# This is because the patch breaks runserver.
if os.environ.get("EVENTLET_NOPATCH") != 'True':
    eventlet.monkey_patch()

# Download latest webpack-stats.json from S3
# before starting WSGI
WEBPACK_STATS_URL = "https://{}/static/webpack-stats.json".format(
    settings.AWS_S3_CUSTOM_DOMAIN
)
WEBPACK_STATS_LOC = os.path.relpath('../static/webpack-stats.json')
with urllib.request.urlopen(WEBPACK_STATS_URL) as response:
    with open(WEBPACK_STATS_LOC, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

application = get_wsgi_application()
