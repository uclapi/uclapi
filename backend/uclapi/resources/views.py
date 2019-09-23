import os
import requests

from lxml import etree

from common.decorators import uclapi_protected_endpoint
from common.helpers import PrettyJsonResponse as JsonResponse

from rest_framework.decorators import api_view


@api_view(['GET'])
@uclapi_protected_endpoint(
    last_modified_redis_key=None
)
def get_pc_availability(request, *args, **kwargs):
    try:
        r = requests.get(os.environ["PCA_LINK"])
    except requests.exceptions.MissingSchema:
        resp = JsonResponse({
            "ok": False,
            "error": ("Could not retrieve availability data."
                      " Please try again later or contact us for support.")
        }, custom_header_data=kwargs)
        resp.status_code = 400
        return resp

    try:
        e = etree.fromstring(r.content)
    except (ValueError, etree.XMLSyntaxError):
        resp = JsonResponse({
            "ok": False,
            "error": ("Could not parse the desktop availability data."
                      " Please try again later or contact us for support.")
        }, custom_header_data=kwargs)
        resp.status_code = 400
        return resp

    data = []
    for pc in e.findall("room"):
        _ = pc.get
        data.append({
            "location": {
                "roomname": _("location"),
                "room_id": _("rid"),
                "latitude": _("latitude"),
                "longitude": _("longitude"),
                "building_name": _("buildingName"),
                "address": _("buildingAddress"),
                "postcode": _("buildingPostcode")
            },
            "free_seats": _("free"),
            "total_seats": _("seats"),
            "room_status": _("info")
        })

    return JsonResponse({
        "ok": True,
        "data": data
    }, custom_header_data=kwargs)
