from django.conf import settings

from rest_framework.decorators import api_view

from common.decorators import uclapi_protected_endpoint
from common.helpers import JsonResponse


@api_view(["GET"])
@uclapi_protected_endpoint(personal_data=False)
def get_rooms(request, *args, **kwargs):
    pass