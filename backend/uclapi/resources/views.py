import os
import requests

from lxml import etree

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse

from rest_framework.decorators import api_view


@api_view(['GET'])
# @uclapi_protected_endpoint()
def get_pc_availability(request, *args, **kwargs):
    try:
        r = requests.get(os.environ["PCA_LINK"])
    except requests.exceptions.MissingSchema:
        return JsonResponse({
            "ok": False,
            "error": "Couldn't get the availability data. Try again later"
        }, rate_limiting_data=kwargs)

    try:
        e = etree.fromstring(r.content)
    except (ValueError, etree.XMLSyntaxError):
        return JsonResponse({
            "ok": False,
            "error": "Couldn't parse the availability data"
        }, rate_limiting_data=kwargs)

    data = []
    for pc in e.findall("room"):
        _ = pc.get
        data.append({
            "location": {
                "room_name": _("location"),
                "room_id": _("rid"),
                "latitude": _("latitude"),
                "longitude": _("longitude"),
                "building_name": _("buildingName"),
                "address": _("buildingAddress"),
                "postcode": _("buildingPostCode")
            },
            "free_seats": _("free"),
            "total_seats": _("seats"),
            "room_status": _("info")
        })

    return JsonResponse({
        "ok": True,
        "data": data
    }, rate_limiting_data=kwargs)
