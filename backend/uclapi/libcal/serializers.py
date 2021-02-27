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


class LibCalIdListSerializer(serializers.Serializer):
    """Serializer for endpoints accept an id or an id list as part of the path"""
    ids = serializers.RegexField(
        r'^\d+(,\d+)*$',
        required=True,  # Default, but stated for clarity.
        help_text='A form id or a list of form ids to retrieve.'
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
