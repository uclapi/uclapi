"""
WSGI config for uclapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from common.helpers import read_dotenv

from django.core.wsgi import get_wsgi_application

read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uclapi.settings")

application = get_wsgi_application()
