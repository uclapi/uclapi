class BadOccupEyeRequest(Exception):
    """
    Custom exception for when any CadCap API request fails.
    This should only be raised by endpoints that could contain
    user-entered data, so that we can give them an error telling
    them that the data they gave us is bad.
    """

    pass


class OccupEyeOtherSensorState(Exception):
    """
    Custom exception that is raised when a sensor is neither
    in the Occupied nor Absent state
    """

    pass
