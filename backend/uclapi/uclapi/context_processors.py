from django.conf import settings

import os


def global_settings(request):
    """
    Sets and makes the WEBPACK_SERVE variable accessible inside templates.
    We use this to decide whether to get static file from STATIC_ROOT or
    localhost:8080 on which webpack-serve runs.
    """
    return {
        'WEBPACK_SERVE': (os.environ["UCLAPI_PRODUCTION"] == "False")
    }
