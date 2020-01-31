import json

from base64 import b64encode
from datetime import datetime, timedelta
from distutils.util import strtobool

import redis
import requests

from common.helpers import LOCAL_TIMEZONE

from django.conf import settings

from .api import OccupEyeApi
from .constants import OccupEyeConstants
from .exceptions import OccupEyeOtherSensorState
from .token import get_bearer_token
from .utils import (
    authenticated_request,
    is_sensor_occupied
)


class OccupeyeCache():
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self._const = OccupEyeConstants()

        access_token = self._redis.get(
            self._const.ACCESS_TOKEN_KEY
        )
        access_token_expiry = self._redis.get(
            self._const.ACCESS_TOKEN_EXPIRY_KEY
        )
        self.bearer_token = get_bearer_token(
            access_token,
            access_token_expiry,
            self._const
        )

    def cache_maps_for_survey(self, survey_id):
        """
        Every Survey (e.g. building) at UCL is comprised of many
        maps. A map may be a floor or wing. This function
        will cache data about those maps in Redis so that it
        can be quickly retrieved later.
        """
        survey_maps_list_key = (
            self._const.SURVEY_MAPS_LIST_KEY
        ).format(survey_id)
        survey_maps_data = authenticated_request(
            self._const.URL_MAPS_BY_SURVEY.format(survey_id),
            self.bearer_token
        )
        pipeline = self._redis.pipeline()

        self.delete_maps(
            pipeline,
            survey_id,
            survey_maps_list_key,
            survey_maps_data
        )

        for survey_map in survey_maps_data:
            survey_map_id = self._const.SURVEY_MAP_DATA_KEY.format(
                survey_id,
                str(survey_map["MapID"])
            )
            pipeline.hmset(
                survey_map_id,
                {
                    "id": survey_map["MapID"],
                    "name": survey_map["MapName"],
                    "image_id": survey_map["ImageID"]
                }
            )
            pipeline.rpush(
                survey_maps_list_key,
                survey_map["MapID"]
            )

        pipeline.execute()

    def cache_survey_data(self):
        """
        This function will cache all surveys (e.g. buildings) in
        the OccupEye system. It makes use of the _cache_maps_for_survey
        helper function above to tie all maps to surveys.
        """
        pipeline = self._redis.pipeline()
        surveys_data = authenticated_request(
            self._const.URL_SURVEYS,
            self.bearer_token
        )
        self.delete_surveys(pipeline, surveys_data)
        for survey in surveys_data:
            # Check whether the survey has been discontinued. If so, we skip
            # over it and refuse to cache it as it is now irrelevant.
            if "EndDate" in survey:
                end_date = datetime.strptime(
                    survey["EndDate"],
                    "%Y-%m-%d"
                ).date()
                if datetime.now().date() > end_date:
                    continue

            survey_id = survey["SurveyID"]
            survey_key = self._const.SURVEY_DATA_KEY.format(
                str(survey_id)
            )
            # We check if the Survey's ID is in our list of staff survey
            # constants. If so, we mark it as such so we can filter them
            # out for students by default.
            staff_survey = str(
                int(survey["SurveyID"]) in self._const.STAFF_SURVEY_IDS
            )
            if survey["Name"] in self._const.SURVEY_LOCATIONS:
                location_data = self._const.SURVEY_LOCATIONS[survey["Name"]]
            else:
                location_data = {
                 "lat": "", "long": "", "address": ["", "", "", ""]
                }
            pipeline.hmset(
                survey_key,
                {
                    "id": survey["SurveyID"],
                    "active": str(survey["Active"]),
                    "name": survey["Name"],
                    "start_time": survey["StartTime"],
                    "end_time": survey["EndTime"],
                    "staff_survey": staff_survey,
                    "lat": location_data["lat"],
                    "long": location_data["long"],
                    "address1": location_data["address"][0],
                    "address2": location_data["address"][1],
                    "address3": location_data["address"][2],
                    "address4": location_data["address"][3]
                }
            )
            pipeline.lpush(
                self._const.SURVEYS_LIST_KEY,
                str(survey_id)
            )
            self.cache_maps_for_survey(survey_id)

        pipeline.execute()

    def cache_image(self, image_id):
        """
        Downloads map images from the API and stores their
        base64 representation and associated data type in Redis.
        """
        headers = {
            "Authorization": self.bearer_token
        }
        url = self._const.URL_IMAGE.format(image_id)
        response = requests.get(
            url=url,
            headers=headers,
            stream=True
        )
        content_type = response.headers['Content-Type']

        raw_image = response.content
        image_b64 = b64encode(raw_image)
        pipeline = self._redis.pipeline()
        pipeline.set(
            self._const.IMAGE_BASE64_KEY.format(image_id),
            image_b64
        )
        pipeline.set(
            self._const.IMAGE_CONTENT_TYPE_KEY.format(image_id),
            content_type
        )
        pipeline.execute()

    def cache_survey_sensors_max_timestamp(self, survey_id):
        """
        Gets the last time the sensor data for the given survey
        was updated. This is delivered back with sensor data
        so that developers can see how recent the data is.
        This is especially important given how much data we
        cache.
        """
        headers = {
            "Authorization": self.get_bearer_token(self._const)
        }
        url = self._const.URL_SURVEY_MAX_TIMESTAMP.format(
            survey_id
        )
        r = requests.get(
            url=url,
            headers=headers
        )
        max_sensor_timestamp = r.text.replace('"', '')
        self._redis.set(
            self._const.SURVEY_MAX_TIMESTAMP_KEY.format(
                survey_id
            ),
            max_sensor_timestamp
        )

    def cache_survey_sensor_data(self, survey_id):
        """
        Caches attribute data about all sensors in a survey
        without matching them to a map.
        This uses the /SurveyDevices endpoint.
        When we actually deliver data to the developer we group
        it by map (so that it is actually useful), so this function
        does not create any lists of sensors (we just cache data
        about each one by ID)
        """
        all_sensors_data = authenticated_request(
            self._const.URL_SURVEY_DEVICES.format(
                survey_id
            ),
            self.bearer_token
        )
        pipeline = self._redis.pipeline()
        survey_sensors_list_key = (
            self._const.SURVEY_SENSORS_LIST_KEY
        ).format(survey_id)
        self.delete_sensors(
            pipeline,
            survey_id,
            survey_sensors_list_key,
            all_sensors_data
        )

        for sensor_data in all_sensors_data:
            hardware_id = sensor_data["HardwareID"]
            sensor_data_key = (
                self._const.SURVEY_SENSOR_DATA_KEY
            ).format(
                survey_id,
                hardware_id
            )

            pipeline.delete(sensor_data_key)
            pipeline.hmset(sensor_data_key, {
                "survey_id": sensor_data["SurveyID"],
                "hardware_id": sensor_data["HardwareID"],
                "survey_device_id": sensor_data["SurveyDeviceID"],
                "host_address": str(sensor_data["HostAddress"]),
                "pir_address": str(sensor_data["PIRAddress"]),
                "device_type": str(sensor_data["DeviceType"]),
                "location": str(sensor_data["Location"]),
                "description_1": str(sensor_data["Description1"]),
                "description_2": str(sensor_data["Description2"]),
                "description_3": str(sensor_data["Description3"]),
                "room_id": sensor_data["RoomID"],
                "room_name": str(sensor_data["RoomName"]),
                "share_id": str(sensor_data["ShareID"]),
                "floor": str(sensor_data["Floor"]),
                "room_type": str(sensor_data["RoomType"]),
                "building_name": str(sensor_data["Building"]),
                "room_description": str(sensor_data["RoomDescription"])
            })

            pipeline.rpush(
                survey_sensors_list_key,
                hardware_id
            )
        pipeline.execute()

    def cache_all_survey_sensor_states(self, survey_id):
        """
        Caches all sensors in a survey, including their latest states
        """
        all_sensors_data = authenticated_request(
            self._const.URL_SURVEY_DEVICES_LATEST.format(
                survey_id
            ),
            self.bearer_token
        )
        if not isinstance(all_sensors_data, list):
            print(
                "[-] Survey {} has bad sensor data, ignoring...".format(
                    survey_id
                )
            )
            return
        pipeline = self._redis.pipeline()
        for sensor_data in all_sensors_data:
            hardware_id = sensor_data["HardwareID"]
            sensor_status_key = (
                self._const.SURVEY_SENSOR_STATUS_KEY
            ).format(survey_id, hardware_id)

            try:
                occupied_state = is_sensor_occupied(
                    sensor_data["LastTriggerType"],
                    sensor_data["LastTriggerTime"]
                )
            except OccupEyeOtherSensorState:
                # This is a rare case, so just set it to False.
                # Easier than expecting our clients to deal with null
                occupied_state = False
            sensor_status = {
                "occupied": str(occupied_state),
                "hardware_id": str(sensor_data["HardwareID"]),
                "last_trigger_type": str(sensor_data["LastTriggerType"]),
                "last_trigger_timestamp": str(sensor_data["LastTriggerTime"])
            }
            pipeline.hmset(sensor_status_key, sensor_status)

        pipeline.execute()

    def cache_sensors_for_map(self, survey_id, map_id):
        """
        Caches a list of every sensor associated with the
        Map ID requested.
        """
        url = self._const.URL_MAPS.format(map_id)
        all_map_sensors_data = authenticated_request(
            url,
            self.bearer_token
        )

        pipeline = self._redis.pipeline()
        map_sensors_list_key = (
            self._const.SURVEY_MAP_SENSORS_LIST_KEY
        ).format(survey_id, map_id)

        pipeline.delete(map_sensors_list_key)

        # Cache a list of every HardwareID associated with the survey map
        # and also sore the co-ordinates of each sensor for when we
        # implement mapping functionality
        for map_sensor_data in all_map_sensors_data["MapItemViewModels"]:
            hardware_id = map_sensor_data["HardwareID"]
            pipeline.rpush(
                map_sensors_list_key,
                hardware_id
            )
            properties_key = (
                self._const.SURVEY_MAP_SENSOR_PROPERTIES_KEY
            ).format(
                survey_id,
                map_id,
                hardware_id
            )
            pipeline.hmset(properties_key, {
                "hardware_id": map_sensor_data["HardwareID"],
                "x_pos": map_sensor_data["X"],
                "y_pos": map_sensor_data["Y"]
            })

        map_vmax_x_key = self._const.SURVEY_MAP_VMAX_X_KEY.format(
            survey_id,
            map_id
        )
        map_vmax_y_key = self._const.SURVEY_MAP_VMAX_Y_KEY.format(
            survey_id,
            map_id
        )
        map_viewbox_key = (
            self._const.SURVEY_MAP_VIEWBOX_KEY
        ).format(
            survey_id,
            map_id
        )
        pipeline.set(
            map_vmax_x_key,
            all_map_sensors_data["VMaxX"]
        )
        pipeline.set(
            map_vmax_y_key,
            all_map_sensors_data["VMaxY"]
        )
        pipeline.set(
            map_viewbox_key,
            all_map_sensors_data["ViewBox"]
        )

        pipeline.execute()

    def cache_historical_time_usage_data(self, survey_id, day_count):
        """
        Function to cache in Redis the historical usage data over each 10
        minute time period.
        day_count is the number of days of historical data (from including
        yesterday, but not including today) to cache.
        E.g. if you cache on Tuesday for 7 days, all the data from
        last Sunday to Monday (e.g. yesterday) inclusive will be cached.
        This is to support apps which show historical survey usage data.
        """

        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=day_count - 1)
        url = self._const.URL_QUERY.format(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            survey_id
        )

        response = authenticated_request(
            url,
            self.bearer_token
        )

        slots = {}

        for result in response:
            # There are some hacks here on the CountOcc parameter
            # This is because, for unknown reasons, sometimes OccupEye
            # returns a None result, instead of a 0. We're excluding it
            # here to prevent some nasty TypeErrors from causing us
            # issues during caching.
            if result["TimeSlot"] in slots:
                if result["CountOcc"] is not None:
                    slots[result["TimeSlot"]]["CountOcc"] += result["CountOcc"]
                slots[result["TimeSlot"]]["Results"] += 1
            else:
                slot_data = {
                    "CountTotal": result["CountTotal"],
                    "Results": 1
                }
                if result["CountOcc"] is None:
                    slot_data["CountOcc"] = 0
                else:
                    slot_data["CountOcc"] = result["CountOcc"]

                slots[result["TimeSlot"]] = slot_data

        data = {}
        for key, value in slots.items():
            average = value["CountOcc"] // value["Results"]
            data[key] = {
                "sensors_absent": value["CountTotal"] - average,
                "sensors_occupied": average,
                "sensors_total": value["CountTotal"]
            }

        average_key = (
            self._const.TIMEAVERAGE_KEY
        ).format(survey_id, day_count)

        self._redis.set(
            average_key,
            json.dumps(data, sort_keys=True)
        )

    def cache_common_summaries(self):
        """
        Function to cache common JSON results for /sensors/summary.
        This function can take up to two seconds to run for the whole
        lot, so it makes sense to cache the individual libraries
        and the endpoint for every survey.
        """
        survey_ids = self._redis.lrange(
            self._const.SURVEYS_LIST_KEY,
            0,
            self._redis.llen(self._const.SURVEYS_LIST_KEY)
        )
        surveys = []
        api = OccupEyeApi()
        for survey_id in survey_ids:
            survey_redis_data = self._redis.hgetall(
                self._const.SURVEY_DATA_KEY.format(survey_id)
            )
            survey_data = {
                "id": int(survey_id),
                "name": survey_redis_data["name"],
                "maps": [],
                "staff_survey": strtobool(
                    str(survey_redis_data["staff_survey"])
                ),
                "sensors_absent": 0,
                "sensors_occupied": 0,
                "sensors_other": 0
            }

            '''
            Begin Hotfix

            Cache data for the survey as a whole. This is to fix a bug in
            OccupEye and this code should be removed as soon as the map data
            returns every sensor in a survey. For longevity, once this code
            is removed, the map data should update the survey_data totals
            instead.
            '''
            all_sensors = self._redis.lrange(
                self._const.SURVEY_SENSORS_LIST_KEY.format(survey_id),
                0,
                self._redis.llen(
                    self._const.SURVEY_SENSORS_LIST_KEY.format(survey_id)
                )
            )
            for sensor_hw_id in all_sensors:
                sensor_map = self._redis.hgetall(
                    self._const.SURVEY_SENSOR_STATUS_KEY.format(
                        survey_id,
                        sensor_hw_id
                    )
                )
                if (
                    "last_trigger_type" not in sensor_map or
                    "last_trigger_timestamp" not in sensor_map
                ):
                    continue
                try:
                    occupied = is_sensor_occupied(
                        sensor_map["last_trigger_type"],
                        sensor_map["last_trigger_timestamp"]
                    )
                    if occupied:
                        survey_data["sensors_occupied"] += 1
                    else:
                        survey_data["sensors_absent"] += 1
                except OccupEyeOtherSensorState:
                    survey_data["sensors_other"] += 1

            '''
            End of Hotfix
            '''

            sensors = api.get_survey_sensors(survey_id)
            for survey_map in sensors["maps"]:
                map_data = {
                    "id": int(survey_map["id"]),
                    "name": survey_map["name"],
                    "sensors_absent": 0,
                    "sensors_occupied": 0,
                    "sensors_other": 0
                }
                for hw_id, sensor in survey_map["sensors"].items():
                    if "last_trigger_type" in sensor:
                        try:
                            occupied = is_sensor_occupied(
                                sensor["last_trigger_type"],
                                sensor["last_trigger_timestamp"]
                            )
                            if occupied:
                                map_data["sensors_occupied"] += 1
                            else:
                                map_data["sensors_absent"] += 1
                        except OccupEyeOtherSensorState:
                            map_data["sensors_other"] += 1

                survey_data["maps"].append(map_data)
                # Now cache this in Redis
                # Cache inside a list to match the outer format
                self._redis.set(
                    self._const.SUMMARY_CACHE_SURVEY.format(survey_id),
                    json.dumps(
                        [
                            {**survey_data}
                        ]
                    )
                )
            surveys.append(survey_data)

        # Now we have summary information for every survey
        self._redis.set(
            self._const.SUMMARY_CACHE_ALL_SURVEYS,
            json.dumps(surveys)
        )
        self._redis.set(
            self._const.SUMMARY_CACHE_ALL_STAFF_SURVEYS,
            json.dumps([s for s in surveys if s['staff_survey']])
        )
        self._redis.set(
            self._const.SUMMARY_CACHE_ALL_STUDENT_SURVEYS,
            json.dumps([s for s in surveys if not s['staff_survey']])
        )

    def feed_cache(self, full):
        """
        Function called by the Django management command to feed the Redis
        cache with as much 24-hour valid information as possible. This
        code should be run at night so that commands during the day are
        quicker.
        It can also be run during the day if the code is updated or we are
        notified of any significant changes to Cad-Cap that require a refresh
        during the day.
        """
        if full:
            self.cache_survey_data()

        survey_ids = self._redis.lrange(
            "occupeye:surveys",
            0,
            self._redis.llen("occupeye:surveys") - 1
        )
        # Cache all the latest surveys
        print("[+] Surveys")
        for survey_id in survey_ids:
            print("==> Survey ID: " + survey_id)
            if full:
                # Cache a list of every map in the survey
                self.cache_maps_for_survey(survey_id)
                # Cache the data for every sensor in the survey
                self.cache_survey_sensor_data(survey_id)

                survey_maps_key = (
                    self._const.SURVEY_MAPS_LIST_KEY
                ).format(survey_id)
                survey_map_ids = self._redis.lrange(
                    survey_maps_key,
                    0,
                    self._redis.llen(survey_maps_key) - 1
                )
                # Cache data for every map within every survey
                for survey_map_id in survey_map_ids:
                    survey_map = self._redis.hgetall(
                        self._const.SURVEY_MAP_DATA_KEY.format(
                            survey_id,
                            survey_map_id
                        )
                    )
                    # Cache the base64 representation of the raw
                    # image for the survey
                    image_id = int(survey_map["image_id"])
                    self.cache_image(image_id)
                    # Cache a list of every sensor in every map
                    self.cache_sensors_for_map(
                        survey_id,
                        survey_map_id
                    )
                # Cache all the historical data for the last x days
                for day_count in self._const.VALID_HISTORICAL_DATA_DAYS:
                    self.cache_historical_time_usage_data(
                        survey_id,
                        day_count
                    )

            self.cache_all_survey_sensor_states(survey_id)
        print("[+] Summaries")
        self.cache_common_summaries()

        print("[+] Setting Last-Modified key")
        last_modified_key = "http:headers:Last-Modified:Workspaces"

        current_timestamp = datetime.now(LOCAL_TIMEZONE).isoformat(
            timespec='seconds'
        )
        self._redis.set(last_modified_key, current_timestamp)

        print("[+] Done")

    def delete_maps(
        self, pipeline, survey_id,
        survey_maps_list_key, survey_maps_data
    ):
        """Delete maps that no longer exist in a survey"""
        redis_survey_maps_set = set(self._redis.lrange(
            survey_maps_list_key,
            0,
            self._redis.llen(survey_maps_list_key)
        ))
        api_survey_maps_id_set = set(
            [str(survey_map["MapID"]) for survey_map in survey_maps_data]
        )
        maps_to_delete = redis_survey_maps_set - api_survey_maps_id_set

        pipeline.delete(survey_maps_list_key)
        for map_id in maps_to_delete:
            pipeline.delete(
                self._const.SURVEY_MAP_DATA_KEY.format(survey_id, map_id)
            )
            pipeline.delete(
                self._const.SURVEY_MAP_VMAX_X_KEY.format(survey_id, map_id)
            )
            pipeline.delete(
                self._const.SURVEY_MAP_VMAX_Y_KEY.format(survey_id, map_id)
            )
            pipeline.delete(
                self._const.SURVEY_MAP_VIEWBOX_KEY.format(survey_id, map_id)
            )
            survey_maps_sensors_key = (
                self._const.SURVEY_MAP_SENSORS_LIST_KEY.format(
                    survey_id,
                    map_id
                )
            )
            survey_maps_sensors_list = self._redis.lrange(
                survey_maps_sensors_key,
                0,
                self._redis.llen(survey_maps_sensors_key)
            )
            for sensor_id in survey_maps_sensors_list:
                pipeline.delete(
                    self._const.SURVEY_MAP_SENSOR_PROPERTIES_KEY.format(
                        survey_id,
                        map_id,
                        sensor_id
                    )
                )
            image_id = self._redis.hgetall(
                self._const.SURVEY_MAP_DATA_KEY.format(survey_id, map_id)
            )['image_id']
            self.delete_image(pipeline, image_id)

            pipeline.delete(survey_maps_sensors_key)

    def delete_surveys(self, pipeline, surveys_data):
        """Delete surveys that no longer exist"""
        redis_survey_set = set(self._redis.lrange(
            self._const.SURVEYS_LIST_KEY,
            0,
            self._redis.llen(self._const.SURVEYS_LIST_KEY)
        ))
        api_survey_id_set = set(
            [str(survey["SurveyID"]) for survey in surveys_data]
        )
        surveys_to_delete = redis_survey_set - api_survey_id_set

        for survey in surveys_data:
            # Check whether the survey has been discontinued.
            # If so, we refuse to cache it as it is now irrelevant.
            if "EndDate" in survey:
                end_date = datetime.strptime(
                    survey["EndDate"],
                    "%Y-%m-%d"
                ).date()
                if datetime.now().date() > end_date:
                    surveys_to_delete.add(str(survey["SurveyID"]))

        pipeline.delete(self._const.SURVEYS_LIST_KEY)
        for survey_id in surveys_to_delete:
            pipeline.delete(self._const.SURVEY_DATA_KEY.format(survey_id))
            pipeline.delete(self._const.SUMMARY_CACHE_SURVEY.format(survey_id))
            pipeline.delete(
                self._const.SURVEY_MAX_TIMESTAMP_KEY.format(survey_id)
            )

            survey_maps_list_key = self._const.SURVEY_MAPS_LIST_KEY.format(
                survey_id
            )
            self.delete_maps(pipeline, survey_id, survey_maps_list_key, [])

            survey_sensors_list_key = (
                self._const.SURVEY_SENSORS_LIST_KEY.format(survey_id)
            )
            self.delete_sensors(
                pipeline,
                survey_id,
                survey_sensors_list_key,
                []
            )

    def delete_sensors(
        self, pipeline, survey_id,
        survey_sensors_list_key, all_sensors_data
    ):
        """Delete sensors that no longer exist in a survey"""
        redis_survey_sensors_set = set(self._redis.lrange(
            survey_sensors_list_key,
            0,
            self._redis.llen(survey_sensors_list_key)
        ))
        api_survey_sensors_id_set = set(
            [str(survey_sensor["HardwareID"]) for survey_sensor in all_sensors_data]  # noqa
        )
        sensors_to_delete = (
            redis_survey_sensors_set - api_survey_sensors_id_set
        )
        pipeline.delete(survey_sensors_list_key)
        for sensor_id in sensors_to_delete:
            pipeline.delete(
                self._const.SURVEY_SENSOR_DATA_KEY.format(survey_id, sensor_id)
            )
            pipeline.delete(
                self._const.SURVEY_SENSOR_STATUS_KEY.format(
                    survey_id, sensor_id
                )
            )

    def delete_image(self, pipeline, image_id):
        "Deletes images that no longer are used by the API"""
        pipeline.delete(self._const.IMAGE_BASE64_KEY.format(image_id))
        pipeline.delete(self._const.IMAGE_CONTENT_TYPE_KEY.format(image_id))
