from rest_framework import serializers

"""
This file contains serializers for LibCal. These are designed to validate the
GET parameters that are passed to us, before they reach LibCal.

This is primarily to defend against the threat model of an attacker who has no
valid OAuth token attempting to exploit a potential vulnerability in the way
LibCal may parse HTTP GET parameters. Doing this without proxying UCL API may
not work, as LibCal would likely reject the request before even processing the
HTTP GET parameters due to the attacker not having a valid token.

NOTE: Not all parameters passed as GET parameters to UCL API are passed as GET
parameters to LibCal. Some LibCal endpoints accept an id or a list of ids as
part of the URL path. For these endpoints we establish an "ids" field in the
serializer. views._libcal_request_forwarder() will then correctly put the "ids"
field in the path, and make sure it isn't accidentally included as part of the
GET parameters.

Each serializer specifies a whitelist of GET parameters and valid values based
on the LibCal documentation.
"""


class LibCalLocationGETSerializer(serializers.Serializer):
    """Serializer for the /1.1/space/locations endpoint"""
    details = serializers.IntegerField(
        min_value=0,
        max_value=1,
        required=False,
        help_text='Flag to indicate you want additional details such as terms and conditions.'
    )


class LibCalIdSerializer(serializers.Serializer):
    """Serializer for endpoints accept a singular id"""
    ids = serializers.IntegerField(
        required=True,
        min_value=0,
        help_text='An id to retrieve'
    )


class LibCalIdListSerializer(serializers.Serializer):
    """Serializer for endpoints accept an id or an id list as part of the path"""
    ids = serializers.RegexField(
        r'^\d+(,\d+)*$',
        required=True,  # Default, but stated for clarity.
        help_text='A form id or a list of form ids to retrieve.'
    )


class LibCalBookingIdListSerializer(serializers.Serializer):
    """Serializer for endpoints accept a booking id or an booking id list as part of the path"""
    ids = serializers.RegexField(
        r'^\w+(,\w+)*$',
        required=True,  # Default, but stated for clarity.
        help_text='A booking id or a list of booking ids to cancel.'
    )


class LibCalCategoryGETSerializer(LibCalIdListSerializer):
    """Serializer for the /1.1/space/category endpoint"""
    details = serializers.IntegerField(
        min_value=0,
        max_value=1,
        required=False,
        help_text=(
            'Flag to indicate you want additional details such as terms and conditions.'
            'Note: This should only be used for systems that do not contain thousands of spaces.'
        )
    )
    availability = serializers.RegexField(
        # TODO: Update regex when we reach the year 10000
        regex='(^next$)|(^[0-9]{4}-[0-9]{2}-[0-9]{2}(,[0-9]{4}-[0-9]{2}-[0-9]{2})?$)',
        required=False,
        help_text=(
            'Either a single date, or a comma separated list of 2 dates (a start and end date).' \
            'The keyword "next" can be used to return availability for the next date that this item is available.' \
            'Note: Setting this value also sets the details value to true.'
        )
    )


class LibCalItemGETSerializer(LibCalIdListSerializer):
    """Serializer for the /1.1/space/item endpoint"""
    availability = serializers.RegexField(
        # TODO: Update regex when we reach the year 10000
        regex='(^next$)|(^[0-9]{4}-[0-9]{2}-[0-9]{2}(,[0-9]{4}-[0-9]{2}-[0-9]{2})?$)',
        required=False,
        help_text=(
            'Either a single date, or a comma separated list of 2 dates (a start and end date).' \
            'The keyword "next" can be used to return availability for the next date that this item is available.'
        )
    )


class LibCalNicknameGETSerializer(LibCalIdListSerializer):
    """Serializer for the /1.1/space/nickname endpoint"""
    date = serializers.DateField(required=False)


class LibCalUtilizationGETSerializer(LibCalIdSerializer):
    """Serializer for the /api/1.1/space/utilization endpoint"""
    categoryId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='Pass a category id here to only show utilization for that category.'
    )
    zoneId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='Pass a zone id here to only show utilization for that zone.'
    )


class LibCalSeatGETSerializer(LibCalIdSerializer):
    """Serializer for the /api/1.1/space/seat endpoint"""
    availability = serializers.RegexField(
        # TODO: Update regex when we reach the year 10000
        regex='^[0-9]{4}-[0-9]{2}-[0-9]{2}(,[0-9]{4}-[0-9]{2}-[0-9]{2})?$',
        required=False,
        help_text=('Either a single date, or a comma separated list of 2 dates (a start and end date).')
    )


class LibCalSeatsGETSerializer(LibCalIdSerializer):
    """Serializer for the /api/1.1/space/seats endpoint"""
    spaceId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text=(
            'Pass a space id to only show details for this space.'
            'If used with a seatId, the spaceId will be ignored.'
        )
    )
    categoryId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text=(
            'Pass a category id to only show details for this category.'
            'If used with a spaceId or seatId filtering, the categoryId will be ignored.'
        )
    )
    seatId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='Pass a seat id here to only show details for this seat.'
    )
    zoneId = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text=(
            'Pass a zone id here to only show details for this zone.'
            'If used with a spaceId or seatId, the zoneId will be ignored.'
        )
    )
    accessibleOnly = serializers.IntegerField(
        min_value=0,
        max_value=1,
        required=False,
        help_text='Pass an accessible only flag to only return accessible seats.'
    )
    availability = serializers.RegexField(
        # TODO: Update regex when we reach the year 10000
        regex='^[0-9]{4}-[0-9]{2}-[0-9]{2}(,[0-9]{4}-[0-9]{2}-[0-9]{2})?$',
        required=False,
        help_text='Either a single date, or a comma separated list of 2 dates (a start and end date).'
    )
    pageIndex = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='For results pagination, this sets which page to receive (starting at 0 for the first page).'
    )
    pageSize = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        help_text='For results pagination, this sets how many results per page to retrieve.'
    )


class LibCalBookingsGETSerializer(serializers.Serializer):
    """Serializer for the /1.1/space/bookings endpoint"""
    eid = serializers.RegexField(
        regex=r'^\d+(,\d+)*$',
        required=False,
        help_text='Pass an item id or list of item ids here to only show bookings for those spaces.'
    )
    seat_id = serializers.RegexField(
        regex=r'^\d+(,\d+)*$',
        required=False,
        help_text='Pass a seat id or list of seat ids here to only show bookings for those seats.'
    )
    cid = serializers.RegexField(
        regex=r'^\d+(,\d+)*$',
        required=False,
        help_text='Pass a category id or list of category ids here to only show bookings for those categories.'
    )
    lid = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='Pass a location id here to only show bookings for that location.'
    )
    date = serializers.DateField(
        required=False,
        help_text='The date to retrieve bookings. Dates in the past are ignored.'
    )
    days = serializers.IntegerField(
        min_value=0,
        max_value=365,
        required=False,
        help_text='The number of days into the future to retrieve bookings from, starting from [date] parameter.'
    )
    limit = serializers.IntegerField(
        min_value=1,
        max_value=500,
        required=False,
        help_text='How many bookings to return, max value is 500.'
    )


class LibCalPersonalBookingsGETSerializer(LibCalBookingsGETSerializer):
    """Serializer for the /1.1/space/bookings endpoint (that shows personal bookings)."""
    email = serializers.EmailField(
        required=True,  # Default, but stated for clarity.
        help_text='Pass an email address to only show bookings made by that patron.'
    )
    formAnswers = serializers.IntegerField(
        min_value=0,
        max_value=1,
        required=False,
        help_text=(
            'Flag to indicate if you want custom form answers to be returned. You can hit the /equipment/question'
            'endpoint to retrieve the details of the booking form questions.'
        )
    )


class BookingSerializer(serializers.Serializer):
    """Serializes a single booking for the /1.1/space/reserve endpoint"""
    id = serializers.IntegerField(
        min_value=0,
        required=True,
        help_text='Pass a location id here to only show bookings for that location.'
    )
    seat_id = serializers.IntegerField(
        min_value=0,
        required=False,
        help_text='Pass a location id here to only show bookings for that location.'
    )
    to = serializers.DateTimeField(
        required=True,
        help_text='Booking end date/time in ISO8601 format.')


class LibCalReservationPOSTSerializer(serializers.Serializer):
    """Serializes bookings for the /1.1/space/reserve endpoint"""
    start = serializers.DateTimeField(
        required=True,
        help_text='Booking start date/time in ISO8601 format.'
    )
    fname = serializers.CharField(
        max_length=100,
        required=True,
        help_text='First name of person making the booking.'
    )
    lname = serializers.CharField(
        max_length=100,
        required=True,
        help_text='Last name of person making the booking.'
    )
    test = serializers.IntegerField(
        min_value=0,
        max_value=1,
        help_text=(
            'A flag to indicate if this is a test booking. If this flag is set the system will process the booking'
            'rules but not actually make the booking. This is a useful feature when developing an application that'
            'makes use of the booking API.'
        )
    )
    email = serializers.EmailField(
        required=True,
        help_text='Email address of person making the booking.'
    )
    nickname = serializers.CharField(
        max_length=100,
        required=False,
        help_text='If your space has "Public Nicknames" enabled, then supply the Nickname field via this parameter'
    )
    # TODO: custom form question ids????? See LibCal API Docs.
    bookings = BookingSerializer(many=True)
