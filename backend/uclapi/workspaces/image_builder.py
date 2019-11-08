import redis

from lxml import etree
from django.conf import settings

from .occupeye.api import OccupEyeApi
from .occupeye.exceptions import BadOccupEyeRequest, OccupEyeOtherSensorState
from .occupeye.utils import is_sensor_occupied


class ImageBuilder():
    """
    Builds an SVG image with live sensor statuses/
    """

    def __init__(self, survey_id, map_id):
        # Confirm integers
        if not survey_id.isdigit():
            raise BadOccupEyeRequest
        if not map_id.isdigit():
            raise BadOccupEyeRequest

        self._api = OccupEyeApi()

        if not self._api.check_map_exists(survey_id, map_id):
            raise BadOccupEyeRequest

        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self._sensors = self._api.get_survey_sensors(
            survey_id
            # return_states=True
        )
        self._survey_id = survey_id
        self._map_id = map_id

        # Set the defaults
        self.set_colours()
        self.set_image_scale()
        self.set_circle_radius()

    def set_colours(self, absent="#016810", occupied="#B60202"):
        self._absent_colour = absent
        self._occupied_colour = occupied

    def set_image_scale(self, image_scale=0.02):
        self._image_scale = image_scale

    def set_circle_radius(self, circle_radius=128):
        self._circle_radius = circle_radius

    def get_live_map(self):
        map_data = self._api.get_survey_image_map_data(
            self._survey_id,
            self._map_id
        )
        nsmap = {
            None: "http://www.w3.org/2000/svg",
            "xlink": "http://www.w3.org/1999/xlink",
            "ev": "http://www.w3.org/2001/xml-events"
        }
        svg = etree.Element(
            "svg",
            nsmap=nsmap
        )
        viewport = etree.SubElement(svg, "g")
        scale = "scale({}, {})".format(
            self._image_scale,
            self._image_scale
        )
        viewport.attrib["transform"] = scale
        base_map = etree.SubElement(viewport, "image")

        # ViewBox data looks like this: 0 0 12345 67890
        # We care about the last two numbers, the width and height
        viewbox_data = map_data["ViewBox"].split(" ")
        base_map.attrib["width"] = viewbox_data[2]
        base_map.attrib["height"] = viewbox_data[3]

        map_data = self._redis.hgetall(
            "occupeye:surveys:{}:maps:{}".format(
                self._survey_id,
                self._map_id
            )
        )
        (b64_data, content_type) = self._api.get_image(
            map_data["image_id"]
        )
        base_map.attrib["{http://www.w3.org/1999/xlink}href"] = (
            "data:{};base64,{}".format(
                content_type,
                b64_data
            )
        )
        bubble_overlay = etree.SubElement(viewport, "g")

        # Get the sensors for that map
        the_map = {}
        for map_obj in self._sensors["maps"]:
            if map_obj["id"] == self._map_id:
                the_map = map_obj
                break

        for sensor_id, sensor_data in the_map["sensors"].items():
            node = etree.SubElement(bubble_overlay, "g")
            node.attrib["id"] = sensor_id
            node.attrib["transform"] = "translate({},{})".format(
                sensor_data["x_pos"],
                sensor_data["y_pos"]
            )
            circle = etree.SubElement(node, "circle")
            circle.attrib["r"] = str(self._circle_radius)
            try:
                occupied = is_sensor_occupied(
                    sensor_data["last_trigger_type"],
                    sensor_data["last_trigger_timestamp"]
                )
            except OccupEyeOtherSensorState:
                # If the sensor is in a strange state just treat
                # it as a free space.
                occupied = False
            except KeyError:
                # Fix for API-4Y, i.e. UCL added a sensor called 'HOST653'
                # which isn't actually a sensor. Hence the sensor status
                # doesn't exist...
                occupied = False
                circle.attrib["opacity"] = "0"

            if occupied:
                circle.attrib["fill"] = self._occupied_colour
            else:
                circle.attrib["fill"] = self._absent_colour

        return etree.tostring(svg, pretty_print=True)
