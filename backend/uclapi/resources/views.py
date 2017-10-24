from django.shortcuts import render
import requests
import xml.etree.ElementTree
from roombookings.helpers import PrettyJsonResponse as JsonResponse
from rest_framework.decorators import api_view
from roombookings.decorators import does_token_exist

@api_view(["GET"])
@does_token_exist
def get_pc_availability(request):
    r = requests.get("https://campusm.ucl.ac.uk/clusterpc_services/presentation_services_v1/pc_availability_v1.xml")
    try:
        e =  xml.etree.ElementTree.fromstring(r.content.decode())
    except xml.etree.ElementTree.ParseError:
        return JsonResponse({
            "ok": False,
            "error": "Couldn't parse the availability data"
        })
    data = []
    for pc in e.findall("room"):
        _ = pc.get
        data.append({
            "location": {
                "room": _("location"),
                "room_id": _("rid"),
                "latitude": _("latitude"),
                "longitude": _("longitude"),
                "building_name": _("buildingName"),
                "address": _("buildingAddress"),
                "postcode": _("buildingPostCode")
            },
            "free_seats": _("free"),
            "total_seats": _("seats"),
            "info": _("info")
        })
    return JsonResponse({
        "ok": True,
        "data": data
    })