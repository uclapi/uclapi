import json

from collections import OrderedDict
from distutils.util import strtobool

import redis

from django.conf import settings

from .constants import OccupEyeConstants
from .exceptions import BadOccupEyeRequest, OccupEyeOtherSensorState
from .utils import (
    is_sensor_occupied,
    survey_ids_to_surveys
)


class OccupEyeApi():
    """
    Python API for the Cad-Capture OccupEye backend.
    Data is cached as much as possible in Redis for performance.
    Instead of having expiring data, it will just be replaced
    at each cache operation.
    """

    def __init__(self):
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self._const = OccupEyeConstants()

    def get_surveys(self, survey_filter):
        """
        Serialises all surveys and maps to a dictionary
        object that can be returned to the user. If the
        requisite data does not exist in Redis, it is cached using
        the helper functions above, then returned from the cache.
        """
        survey_ids = self._redis.lrange(
            self._const.SURVEYS_LIST_KEY,
            0,
            self._redis.llen(self._const.SURVEYS_LIST_KEY) - 1
        )

        surveys = []
        for survey_id in survey_ids:
            survey_data = self._redis.hgetall(
                self._const.SURVEY_DATA_KEY.format(survey_id)
            )
            survey = {
                "id": int(survey_data["id"]),
                "name": survey_data["name"],
                "active": strtobool(survey_data["active"]),
                "start_time": survey_data["start_time"],
                "end_time": survey_data["end_time"],
                "staff_survey": strtobool(survey_data["staff_survey"]),
                "location": {
                    "coordinates": {
                        "lat": survey_data["lat"],
                        "lng": survey_data["long"]
                        },
                    "address": [
                        survey_data["address1"],
                        survey_data["address2"],
                        survey_data["address3"],
                        survey_data["address4"]
                        ]
                    }
                }
            # If we want to filter out staff surveys and this is a staff
            # one then we skip over it.
            if (
                survey_filter == "student" and survey["staff_survey"] or
                survey_filter == "staff" and not survey["staff_survey"]
            ):
                continue

            survey_maps_list_key = self._const.SURVEY_MAPS_LIST_KEY.format(
                survey_id
            )
            survey_map_count = self._redis.llen(
                survey_maps_list_key
            ) - 1
            survey_maps_ids_list = self._redis.lrange(
                survey_maps_list_key,
                0,
                survey_map_count
            )

            survey_maps = []
            for survey_map_id in survey_maps_ids_list:
                survey_map = self._redis.hgetall(
                    self._const.SURVEY_MAP_DATA_KEY.format(
                        survey_id,
                        survey_map_id
                    )
                )
                survey_maps.append(
                    {
                       "id": int(survey_map["id"]),
                       "name": survey_map["name"],
                       "image_id": int(survey_map["image_id"])
                    }
                )
            survey["maps"] = survey_maps
            surveys.append(survey)
        return surveys

    def get_image(self, image_id):
        """
        Pulls an Image ID requested by the user from Redis.
        """
        # We must ensure that only digits are passed into the code
        # to prevent Redis injection attacks.
        if not image_id.isdigit():
            raise BadOccupEyeRequest

        b64_key = self._const.IMAGE_BASE64_KEY.format(
            image_id
        )
        if not self._redis.exists(b64_key):
            raise BadOccupEyeRequest

        content_type_key = self._const.IMAGE_CONTENT_TYPE_KEY.format(
            image_id
        )

        image_b64 = self._redis.get(b64_key)
        content_type = self._redis.get(content_type_key)

        return (image_b64, content_type)

    def get_survey_sensor_max_timestamp(self, survey_id):
        """
        Retrieves the max sensor timestamp from cache.
        """
        max_timestamp_key = self._const.SURVEY_MAX_TIMESTAMP_KEY.format(
            survey_id
        )
        if self._redis.exists(max_timestamp_key):
            return self._redis.get(max_timestamp_key)
        else:
            raise BadOccupEyeRequest

    def get_survey_sensors(self, survey_id):
        """
        Gets all sensors in a survey and returns their statuses
        """
        # Check whether the Survey ID requested is actually
        # an integer.
        if isinstance(survey_id, str):
            if not survey_id.isdigit():
                raise BadOccupEyeRequest

        maps_key = self._const.SURVEY_MAPS_LIST_KEY.format(survey_id)
        maps = self._redis.lrange(
            maps_key,
            0,
            self._redis.llen(maps_key) - 1
        )

        survey_data_key = self._const.SURVEY_DATA_KEY.format(survey_id)
        survey_data = self._redis.hgetall(survey_data_key)

        data = {
            "maps": [],
            "survey_id": survey_data["id"],
            "survey_name": survey_data["name"]
        }

        all_survey_sensors_key = (
            self._const.SURVEY_SENSORS_LIST_KEY
        ).format(survey_id)

        survey_sensors_ids = self._redis.lrange(
            all_survey_sensors_key,
            0,
            self._redis.llen(all_survey_sensors_key)
        )

        pipeline = self._redis.pipeline()

        # Dictionary with the general :data for for every sensor
        # in the survey with no regard for map
        survey_sensors_data = dict()
        for sensor_id in survey_sensors_ids:
            sensor_data_key = (
                self._const.SURVEY_SENSOR_DATA_KEY
            ).format(survey_id, sensor_id)
            pipeline.hgetall(sensor_data_key)

        for sensor_data in pipeline.execute():
            survey_sensors_data[sensor_data["hardware_id"]] = sensor_data

        for map_id in maps:
            map_sensors_key = (
                self._const.SURVEY_MAP_SENSORS_LIST_KEY
            ).format(survey_id, map_id)
            sensor_hw_ids = self._redis.lrange(
                map_sensors_key,
                0,
                self._redis.llen(map_sensors_key) - 1
            )

            sensors = OrderedDict()

            # Get sensor properties requests into a pipeline
            # Whilst at it, grab the :data from survey_sensors_data
            for sensor_id in sensor_hw_ids:
                sensor_properties_key = (
                    self._const.SURVEY_MAP_SENSOR_PROPERTIES_KEY
                ).format(survey_id, map_id, sensor_id)
                pipeline.hgetall(sensor_properties_key)

            # Now execute that pipeline
            for result in pipeline.execute():
                hw_id = result['hardware_id']
                if hw_id in survey_sensors_data:
                    sensors[hw_id] = {**result, **survey_sensors_data[hw_id]}
                else:
                    sensors[hw_id] = result

            # Now do the same thing but for the sensor states
            for sensor_id in sensor_hw_ids:
                sensor_status_key = (
                    self._const.SURVEY_SENSOR_STATUS_KEY
                ).format(survey_id, sensor_id)
                pipeline.hgetall(sensor_status_key)

            for result in pipeline.execute():
                if result:
                    hw_id = result['hardware_id']
                    sensors[hw_id][
                        "last_trigger_timestamp"
                    ] = result["last_trigger_timestamp"]
                    sensors[hw_id][
                        "last_trigger_type"
                    ] = result["last_trigger_type"]
                    try:
                        occupied = is_sensor_occupied(
                            result["last_trigger_type"],
                            result["last_trigger_timestamp"]
                        )
                    except OccupEyeOtherSensorState:
                        occupied = False
                    sensors[hw_id]["occupied"] = occupied

            map_data_key = self._const.SURVEY_MAP_DATA_KEY.format(
                survey_id,
                map_id
            )
            map_data = self._redis.hgetall(map_data_key)
            map_data["sensors"] = sensors
            data["maps"].append(map_data)
        max_timestamp_key = (
            self._const.SURVEY_MAX_TIMESTAMP_KEY
        ).format(survey_id)
        data["most_recent_timestamp"] = self._redis.get(max_timestamp_key)

        return data

    def get_max_survey_timestamp(self, survey_id):
        """
        Get the highest timestamp of any sensor in the OccupEye system.
        This is a shortcut for developers to check whether any data has
        changed.
        If the data is returned from Redis then it will be in sync
        with the internal cache. If it has to be re-cached into
        Redis by this endpoint then the data has come from OccupEye
        which means there will be no other cached data.
        I have added this explanation just in case we end up scratching
        our heads over this at a later date!
        """
        if not survey_id.isdigit():
            raise BadOccupEyeRequest

        max_timestamp_key = (
            self._const.SURVEY_MAX_TIMESTAMP_KEY
        ).format(survey_id)

        # It's either cached, or it does not exist
        max_timestamp_cached = self._redis.get(max_timestamp_key)
        if max_timestamp_cached:
            return (int(survey_id), max_timestamp_cached)
        else:
            raise BadOccupEyeRequest

    def _get_survey_sensors_data_worker(
        self,
        survey_id,
        survey_name,
        shared_dict
    ):
        survey_data = {
            "id": survey_id,
            "name": survey_name,
            "maps": []
        }
        sensors = self.get_survey_sensors(survey_id)
        for survey_map in sensors["maps"]:
            map_data = {
                "id": survey_map["id"],
                "name": survey_map["name"],
                "sensors_absent": 0,
                "sensors_occupied": 0,
                "sensors_other": 0
            }
            for _, sensor in survey_map["sensors"].items():
                # We only care about sensors with a trigger event.
                # Without this, the data is useless (and probably bogus)
                # so we gracefully skip over it and hope for the best.
                if "last_trigger_type" not in sensor:
                    continue

                try:
                    sensor_occupied = is_sensor_occupied(
                        sensor["last_trigger_type"],
                        sensor["last_trigger_timestamp"]
                    )
                    if sensor_occupied:
                        map_data["sensors_occupied"] += 1
                    else:
                        map_data["sensors_absent"] += 1
                except OccupEyeOtherSensorState:
                    # If the seat is neither occupied nor absent, consider
                    # it to be in some other state
                    map_data["sensors_other"] += 1

            survey_data["maps"].append(map_data)
        shared_dict[survey_id] = survey_data

    def get_survey_sensors_summary(self, survey_ids, survey_filter):
        """
        Gets a summary of every survey, map and the sensor counts within them.
        """
        surveys_data = self.get_surveys(survey_filter)
        filtered_surveys = survey_ids_to_surveys(
            surveys_data,
            survey_ids
        )

        # Check whether every survey was requested
        if len(filtered_surveys) == len(surveys_data):
            # Since the list is de-duplicated and clean, we can return
            # data for all surveys straight from the cache if the list
            # of Survey IDs is the same length as the total surveys
            # available.
            if survey_filter == "all":
                data = json.loads(
                    self._redis.get(
                        self._const.SUMMARY_CACHE_ALL_SURVEYS
                    )
                )
            elif survey_filter == "student":
                data = json.loads(
                    self._redis.get(
                        self._const.SUMMARY_CACHE_ALL_STUDENT_SURVEYS
                    )
                )
            elif survey_filter == "staff":
                data = json.loads(
                    self._redis.get(
                        self._const.SUMMARY_CACHE_ALL_STAFF_SURVEYS
                    )
                )
            else:
                raise BadOccupEyeRequest
            return data

        # If we got here, the user specified one or more survey_ids.
        # Combine the cache data to service the request.

        summary_list = []
        for survey in filtered_surveys:
            survey_id = int(survey["id"])
            cache_key = self._const.SUMMARY_CACHE_SURVEY.format(
                survey_id
            )
            survey_data = json.loads(
                self._redis.get(cache_key)
            )
            summary_list.extend(survey_data)

        return summary_list

    def get_historical_time_usage_data(
        self,
        survey_ids,
        day_count,
        survey_filter
    ):
        surveys_data = self.get_surveys(survey_filter)

        filtered_surveys = survey_ids_to_surveys(
            surveys_data,
            survey_ids
        )

        data = []

        for survey in filtered_surveys:
            timeaverage_key = (
                self._const.TIMEAVERAGE_KEY
            ).format(survey["id"], day_count)
            averages = json.loads(
                self._redis.get(timeaverage_key)
            )
            survey_data = {
                "survey_id": survey["id"],
                "name": survey["name"],
                "averages": averages
            }
            data.append(survey_data)

        return data

    def get_survey_image_map_data(self, survey_id, map_id):
        """
        Gets information needed by the Image Builder to create a
        .SVG file showing the state of every library sensor
        """
        map_vmax_x_key = (
            self._const.SURVEY_MAP_VMAX_X_KEY
        ).format(
            survey_id,
            map_id
        )
        map_vmax_y_key = (
            self._const.SURVEY_MAP_VMAX_Y_KEY
        ).format(
            survey_id,
            map_id
        )
        map_viewbox = (
            self._const.SURVEY_MAP_VIEWBOX_KEY
        ).format(
            survey_id,
            map_id
        )
        map_vmax_x = self._redis.get(map_vmax_x_key)
        map_vmax_y = self._redis.get(map_vmax_y_key)
        map_viewbox = self._redis.get(map_viewbox)

        data = {
            "VMaxX": map_vmax_x,
            "VMaxY": map_vmax_y,
            "ViewBox": map_viewbox
        }

        return data

    def check_survey_exists(self, survey_id):
        survey_data_key = self._const.SURVEY_DATA_KEY.format(
            survey_id
        )
        return self._redis.exists(survey_data_key)

    def check_map_exists(self, survey_id, map_id):
        map_data_key = self._const.SURVEY_MAP_DATA_KEY.format(
            survey_id,
            map_id
        )
        return self._redis.exists(map_data_key)
