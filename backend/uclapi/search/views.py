from rest_framework.decorators import api_view
from django.http import JsonResponse

from roombookings.decorators import does_token_exist, log_api_call, throttle

import os
import requests


@api_view(['GET'])
@does_token_exist
@throttle
@log_api_call
def people(request):
    if "name" not in request.GET:
        return JsonResponse({
            "ok": False,
            "error": "Required param name not provided"
        })

    query = request.GET["name"]

    url = (
        "{}?query={}"
        "&collection=website-meta&profile=_directory&tab=directory"
        "&num_ranks=10000"
        .format(
            os.environ["SEARCH_API_URL"],
            query
        )
    )

    r = requests.get(url)

    results = r.json()["response"]["resultPacket"]["results"][:20]

    def serialize_person(person):
        return {
            "name": person["title"],
            "department": person["metaData"]["7"],
            "email": person["metaData"]["E"],
            "status": person["metaData"]["g"]
        }

    people = []
    for person in results:
        people.append(serialize_person(person))

    return JsonResponse({
        "ok": False,
        "people": people
    })
