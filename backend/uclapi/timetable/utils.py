from roombookings.models import Location, SiteLocation


SESSION_TYPE_MAP = {
    "EX": "Examination",
    "L": "Lecture",
    "P": "Practical",
    "PBL": "Problem Based Learning",
}

_site_coord_cache = {}
_room_coord_cache = {}


def get_location_coordinates(siteid, roomid):
    """
    Given a site and room, returns the co-ordinates of this location.

    :param siteid:
    :type siteid: str
    :param roomid:
    :type roomid: str

    :raise Location.DoesNotExist: If the site can not be found

    :returns: latitude and longitude, or None,None in failure to
              raise exception
    :rtype: tuple (str,str)
    """
    # First try and get the specific room's location
    try:
        if roomid in _room_coord_cache:
            return _room_coord_cache[roomid]
        location = Location.objects.get(
            siteid=siteid,
            roomid=roomid
        )
        _room_coord_cache[roomid] = (location.lat, location.lng)
        return location.lat, location.lng
    except Location.DoesNotExist:
        pass

    # Now try and get the building's location
    try:
        if siteid in _site_coord_cache:
            return _site_coord_cache[siteid]
        location = SiteLocation.objects.get(
            siteid=siteid
        )
        _site_coord_cache[siteid] = (location.lat, location.lng)
        return location.lat, location.lng
    except SiteLocation.DoesNotExist:
        pass

    # Now just bail
    return None, None
