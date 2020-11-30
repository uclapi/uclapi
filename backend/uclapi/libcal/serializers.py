from rest_framework import serializers

"""
This file contains serializers for LibCal. These are designed to validate the
GET parameters that are passed to us, before they reach LibCal.

This is primarily to defend against the threat model of an attacker who has no
valid OAuth token attempting to exploit a potential vulnerability in the way
LibCal may parse HTTP GET parameters. Doing this without proxying UCL API may
not work, as LibCal would likely reject the request before even processing the
HTTP GET parameters due to the attacker not having a valid token.

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
