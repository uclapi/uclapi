from rest_framework.decorators import api_view

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse

import os
import requests


@api_view(['GET'])
@uclapi_protected_endpoint(
    last_modified_redis_key=None  # Served directly from the backend Search API
)
def people(request, *args, **kwargs):
    if "query" not in request.GET:
        response = JsonResponse({
            "ok": False,
            "error": "No query provided."
        }, custom_header_data=kwargs)
        response.status_code = 400
        return response

    query = request.GET["query"]

    url = (
        "{}?{}={}"
        .format(
            os.environ["SEARCH_API_URL"],
            os.environ["SEARCH_API_QUERY_PARAMS"],
            query,
        )
    )

    r = requests.get(url)

    results = r.json()["response"]["resultPacket"]["results"][:20]

    def serialize_person(person):
        return {
            "name": person["title"],
            "department": person["metaData"].get("7", ""),
            "email": person["metaData"].get("E", ""),
            "status": person["metaData"].get("g", ""),
        }

    people = [serialize_person(person) for person in results]

    return JsonResponse({
        "ok": True,
        "people": people
    }, custom_header_data=kwargs)
