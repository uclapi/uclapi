from functools import wraps

from .occupeye import OccupEyeApi

def occupeye_api_request():
    def occupeye_request(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            api = OccupEyeApi()
            # Make the API objects available to the function this
            # decorator is attached to
            kwargs['OccupEyeApi'] = api

            return view_func(request, *args, **kwargs)
        return wrapped
    return occupeye_request
