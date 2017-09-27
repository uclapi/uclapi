from rest_framework.decorators import api_view
from django.http import JsonResponse

from roombookings.decorators import does_token_exist, log_api_call, throttle


@api_view(['GET'])
@does_token_exist
@throttle
@log_api_call
def people(request, *args, **kwargs):
    return JsonResponse({
        "ok": True,
        "people": "Work in Progress"
    })
