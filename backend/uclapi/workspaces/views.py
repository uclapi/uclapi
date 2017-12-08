from django.conf import settings

from rest_framework.decorators import api_view

from common.decorators import uclapi_protected_endpoint
from common.helpers import JsonResponse

from .decorators import occupeye_api_request


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
@occupeye_api_request()
def get_rooms(request, *args, **kwargs):
    api = kwargs['api']
    return JsonResponse(
        api.get_surveys(),
        rate_limit_data=kwargs
    )
