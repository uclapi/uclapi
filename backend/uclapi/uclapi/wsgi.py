"""
WSGI config for uclapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import errno
import os
import shutil
import time
import urllib.request

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
WEBPACK_STATS_MIN_AGE = 60

should_download_webpack_stats = True
# First we check if the WebPack stats file is too recent.
# If so, we don't even bother trying to overwrite it.
if os.path.isfile(WEBPACK_STATS_LOC):
    file_stats = os.stat(WEBPACK_STATS_LOC)
    file_age = time.time() - file_stats.st_mtime
    if file_age < WEBPACK_STATS_MIN_AGE:
        should_download_webpack_stats = False

if should_download_webpack_stats:
    try:
        with open(WEBPACK_STATS_LOC, 'wb') as out_file:
            with urllib.request.urlopen(WEBPACK_STATS_URL) as response:
                shutil.copyfileobj(response, out_file)
    except IOError as e:
        if e != errno.EACCES or e != errno.EAGAIN:
            raise

application = get_wsgi_application()
