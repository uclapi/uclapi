import json
import os
from base64 import b64encode
from collections import OrderedDict
from time import time as time_now
from multiprocessing import Lock, Manager, Process
import redis
import requests

from django.conf import settings


class BadOccupEyeRequest(Exception):
    """
    Custom exception for when any CadCap API request fails.
    This should only be raised by endpoints that could contain
    user-entered data, so that we can give them an error telling
    them that the data they gave us is bad.
    """
    pass


class OccupEyeApi():
    """
    Python API for the Cad-Capture OccupEye backend.
    Data is cached as much as possible in Redis for performance.
    """
    # Keep general survey data around in the cache for a day
    SURVEY_TTL = 86400

    # Keep image data in the cache for two days
    IMAGE_TTL = 172800

    # Keep sensor data in the cache for a minute
    SENSOR_STATUS_TTL = 60

    def __init__(self, test_mode=False):
        self.r = redis.StrictRedis(
            host=settings.REDIS_UCLAPI_HOST,
            charset="utf-8",
            decode_responses=True
        )
        self.deployment_id = os.environ["OCCUPEYE_DEPLOYMENT_ID"]
        self.deployment_name = os.environ["OCCUPEYE_DEPLOYMENT_NAME"]
        self.base_url = os.environ["OCCUPEYE_BASE_URL"]

        # If either of those variables come up false, make sure
        # we have an access token before we continue.
        # We don't want to do anything manually in test mode to avoid
        # hitting environment variables we may not have yet.
        if test_mode:
            self.access_token = None
            self.access_token_expiry = None
        else:
            self.access_token = self.r.get("occupeye:access_token")

            access_token_expiry = self.r.get("occupeye:access_token_expiry")
            if access_token_expiry:
                self.access_token_expiry = int(access_token_expiry)
            else:
                self.access_token_expiry = None
            if not self.access_token or not self.access_token_expiry:
                self.get_token()

    def _str2bool(self, v):
        """
        Converts a string representation of a boolean
        into an actual boolean object. This is used
        to convert the boolean strings from Redis into
        actual bool objects.
        """
        return str(v).lower() in ("yes", "true", "t", "1")

    def get_token(self):
        """
        Gets a fresh OAuth 2.0 Bearer token based on the
        username and password stored in the environment.
        """
        url = self.base_url + "/token"
        body = {
            "Grant_type": "password",
            "Username": os.environ["OCCUPEYE_USERNAME"],
            "Password": os.environ["OCCUPEYE_PASSWORD"]
        }

        response = requests.post(
            url=url,
            data=body
        )

        response_data = json.loads(response.text)

        self.access_token = response_data["access_token"]
        self.access_token_expiry = int(time_now()) + int(
            response_data["expires_in"]
        )
        self.r.set("occupeye:access_token", self.access_token)
        self.r.set("occupeye:access_token_expiry", self.access_token_expiry)

    def token_valid(self):
        """
        Checks if the token exists and has not expired.
        """
        if not self.access_token:
            return False

        # Ensure the access token has not expired since we last checked
        if time_now() > self.access_token_expiry:
            return False

        return True

    def get_bearer_token(self):
        """
        If a token is valid, it returns the Bearer string
        used in the Authorization header.
        """
        if not self.token_valid():
            self.get_token()

        return "Bearer " + self.access_token

    def _cache_maps_for_survey(self, survey_id):
        """
        Every Survey (e.g. building) at UCL is comprised of many
        maps. A map may be a floor or wing. This function
        will cache data about those maps in Redis so that it
        can be quickly retrieved later.
        """
        survey_maps_key = "occupeye:surveys:{}:maps".format(
            survey_id
        )
        pipeline = self.r.pipeline()
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/Maps/?deployment={}&surveyid={}".format(
            self.base_url,
            self.deployment_name,
            survey_id
        )
        request = requests.get(
            url=url,
            headers=headers
        )
        survey_maps_data = request.json()

        pipeline.delete(survey_maps_key)
        for survey_map in survey_maps_data:
            survey_map_id = "occupeye:surveys:{}:maps:{}".format(
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
                survey_maps_key,
                survey_map["MapID"]
            )
            pipeline.expire(
                survey_map_id,
                self.SURVEY_TTL
            )
        pipeline.expire(
            survey_maps_key,
            self.SURVEY_TTL
        )
        pipeline.execute()

    def _cache_survey_data(self):
        """
        This function will cache all surveys (e.g. buildings) in
        the OccupEye system. It makes use of the _cache_maps_for_survey
        helper function above to tie all maps to surveys.
        """
        # Use a Redis Pipeline to ensure that all the data is inserted together
        # and atomically
        pipeline = self.r.pipeline()
        # Ensure that the list of occupeye surveys has actually been cleared
        pipeline.delete("occupeye:surveys")

        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/Surveys/?deployment={}".format(
            self.base_url,
            self.deployment_name
        )
        response = requests.get(
            url=url,
            headers=headers
        )
        surveys_data = response.json()

        for survey in surveys_data:
            survey_key = "occupeye:surveys:" + str(survey["SurveyID"])
            pipeline.hmset(
                survey_key,
                {
                    "id": survey["SurveyID"],
                    "active": survey["Active"],
                    "name": survey["Name"],
                    "start_time": survey["StartTime"],
                    "end_time": survey["EndTime"]
                }
            )
            pipeline.expire(survey_key, self.SURVEY_TTL)
            # We prepend to the list of Surveys because the API returns
            # a list of surveys where the ID decrements
            pipeline.lpush("occupeye:surveys", str(survey["SurveyID"]))
            # Cache all maps for this survey for later use
            self._cache_maps_for_survey(survey["SurveyID"])

        pipeline.expire("occupeye:surveys", self.SURVEY_TTL)
        pipeline.execute()

    def get_surveys(self):
        """
        Serialises all surveys and maps to a dictionary
        object that can be returned to the user. If the
        requisite data does not exist in Redis, it is cached using
        the helper functions above, then returned from the cache.
        """
        if self.r.llen("occupeye:surveys") == 0:
            # The data is not in the cache, so cache it.
            self._cache_survey_data()

        # Now we know we have the data cached, we can serve it
        survey_ids = self.r.lrange(
            "occupeye:surveys",
            0,
            self.r.llen("occupeye:surveys") - 1
        )

        surveys = []

        for survey_id in survey_ids:
            survey_data = self.r.hgetall("occupeye:surveys:" + survey_id)
            survey = {
                "id": int(survey_data["id"]),
                "name": survey_data["name"],
                "active": self._str2bool(survey_data["active"]),
                "start_time": survey_data["start_time"],
                "end_time": survey_data["end_time"]
            }
            survey_map_ids_list = "occupeye:surveys:{}:maps".format(
                survey_id
            )
            survey_map_ids = self.r.lrange(
                survey_map_ids_list,
                0,
                self.r.llen(survey_map_ids_list) - 1
            )
            survey_maps = []
            for survey_map_id in survey_map_ids:
                survey_map = self.r.hgetall(
                    "occupeye:surveys:{}:maps:{}".format(
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

    def _cache_image(self, image_id):
        """
        Downloads map images from the API and stores their
        base64 representation and associated data type in Redis.
        """
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/images/{}?deployment={}".format(
            self.base_url,
            image_id,
            self.deployment_name
        )
        try:
            response = requests.get(
                url=url,
                headers=headers,
                stream=True
            )
            content_type = response.headers['Content-Type']
        except:
            raise BadOccupEyeRequest

        raw_image = response.content
        image_b64 = b64encode(raw_image)

        pipeline = self.r.pipeline()
        pipeline.set(
            "occupeye:image:{}:base64".format(image_id),
            image_b64
        )
        pipeline.expire(
            "occupeye:image:{}:base64".format(image_id),
            self.IMAGE_TTL
        )
        pipeline.set(
            "occupeye:image:{}:content_type".format(image_id),
            content_type
        )
        pipeline.expire(
            "occupeye:image:{}:content_type".format(image_id),
            self.IMAGE_TTL
        )
        pipeline.execute()

    def get_image(self, image_id):
        """
        Pulls an Image ID requested by the user from Redis.
        """
        # We must ensure that only digits are passed into the code
        # to prevent Redis injection attacks.
        if not image_id.isdigit():
            raise BadOccupEyeRequest

        if not self.r.exists("occupeye:image:{}:base64".format(image_id)):
            self._cache_image(image_id)

        image_b64 = self.r.get("occupeye:image:{}:base64".format(image_id))
        content_type = self.r.get(
            "occupeye:image:{}:content_type".format(image_id)
        )

        return (image_b64, content_type)

    def _get_survey_sensor_max_timestamp(self, survey_id):
        """
        Gets the last time the sensor data for the given survey
        was updated. This is delivered back with sensor data
        so that developers can see how recent the data is.
        This is especially important given how much data we
        cache.
        """
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/SurveyMaxMessageTime/{}?deployment={}".format(
            self.base_url,
            survey_id,
            self.deployment_name
        )
        response = requests.get(
            url=url,
            headers=headers
        )
        # The response has the timeestamp surrounded in double
        # quotes, so we strip those away.
        max_sensor_timestamp = response.text.replace('"', '')
        return max_sensor_timestamp

    def _cache_survey_sensor_data(self, survey_id):
        """
        Caches attribute data about all sensors in a survey
        without matching them to a map.
        This uses the /SurveyDevices endpoint.
        When we actually deliver data to the developer we group
        it by map (so that it is actually useful), so this function
        does not create any lists of sensors (we just cache data
        about each one by ID)
        """
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/SurveyDevices/?deployment={}&surveyid={}".format(
            self.base_url,
            self.deployment_name,
            survey_id
        )
        response = requests.get(
            url=url,
            headers=headers
        )
        all_sensors_data = response.json()
        pipeline = self.r.pipeline()
        survey_sensors_key = "occupeye:surveys:{}:sensors".format(survey_id)
        pipeline.delete(survey_sensors_key)

        for sensor_data in all_sensors_data:
            sensor_data_key = (
                "occupeye:surveys:{}:sensors:{}:data"
            ).format(survey_id, sensor_data["HardwareID"])

            pipeline.hmset(sensor_data_key, {
                "survey_id": sensor_data["SurveyID"],
                "hardware_id": sensor_data["HardwareID"],
                "survey_device_id": sensor_data["SurveyDeviceID"],
                "host_address": sensor_data["HostAddress"],
                "pir_address": sensor_data["PIRAddress"],
                "device_type": sensor_data["DeviceType"],
                "location": sensor_data["Location"],
                "description_1": sensor_data["Description1"],
                "description_2": sensor_data["Description2"],
                "description_3": sensor_data["Description3"],
                "room_id": sensor_data["RoomID"],
                "room_name": sensor_data["RoomName"],
                "share_id": sensor_data["ShareID"],
                "floor": self._str2bool(sensor_data["Floor"]),
                "room_type": sensor_data["RoomType"],
                "building_name": sensor_data["Building"],
                "room_description": sensor_data["RoomDescription"]
            })
            pipeline.rpush(survey_sensors_key, sensor_data["HardwareID"])
            pipeline.expire(sensor_data_key, self.SURVEY_TTL)

        pipeline.expire(survey_sensors_key, self.SURVEY_TTL)
        pipeline.execute()

    def _cache_all_survey_sensor_states(self, survey_id):
        """
        Caches all sensors in a survey, including their latest states
        """
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/SurveySensorsLatest/{}?deployment={}".format(
            self.base_url,
            survey_id,
            self.deployment_name
        )
        response = requests.get(
            url=url,
            headers=headers
        )
        all_sensors_data = response.json()
        pipeline = self.r.pipeline()
        for sensor_data in all_sensors_data:
            sensor_status_key = "occupeye:surveys:{}:sensors:{}:status".format(
                survey_id,
                sensor_data["HardwareID"]
            )
            pipeline.hmset(
                sensor_status_key,
                {
                    "hardware_id": sensor_data["HardwareID"],
                    "last_trigger_type": sensor_data["LastTriggerType"],
                    "last_trigger_timestamp": sensor_data["LastTriggerTime"]
                }
            )
            pipeline.expire(sensor_status_key, self.SENSOR_STATUS_TTL)

        max_timestamp_key = (
            "occupeye:surveys:{}:sensors:max_timestamp"
        ).format(survey_id)
        max_timestamp_value = self._get_survey_sensor_max_timestamp(survey_id)

        pipeline.set(
            max_timestamp_key,
            max_timestamp_value
        )
        pipeline.expire(max_timestamp_key, self.SENSOR_STATUS_TTL)

        pipeline.execute()

    def _cache_sensors_for_map(self, survey_id, map_id):
        """
        Caches a list of every sensor associated with the
        Map ID requested.
        """
        headers = {
            "Authorization": self.get_bearer_token()
        }
        url = "{}/api/Maps/{}?deployment={}&origin=tl".format(
            self.base_url,
            map_id,
            self.deployment_name
        )
        response = requests.get(
            url=url,
            headers=headers
        )
        all_map_sensors_data = response.json()

        pipeline = self.r.pipeline()
        map_sensors_list_key = "occupeye:surveys:{}:maps:{}:sensors".format(
            survey_id,
            map_id
        )
        pipeline.delete(map_sensors_list_key)

        # Cache a list of every HardwareID associated with the survey map
        # and also sore the co-ordinates of each sensor for when we
        # implement mapping functionality
        for map_sensor_data in all_map_sensors_data["MapItemViewModels"]:
            pipeline.rpush(
                map_sensors_list_key,
                map_sensor_data["HardwareID"]
            )
            properties_key = "{}:{}:properties".format(
                map_sensors_list_key,
                map_sensor_data["HardwareID"]
            )
            pipeline.hmset(
                properties_key,
                {
                    "hardware_id": map_sensor_data["HardwareID"],
                    "x_pos": map_sensor_data["X"],
                    "y_pos": map_sensor_data["Y"]
                }
            )
            pipeline.expire(
                properties_key,
                self.SURVEY_TTL
            )

        pipeline.expire(
            map_sensors_list_key,
            self.SENSOR_STATUS_TTL
        )
        pipeline.execute()

    def get_survey_sensors(self, survey_id, return_states=True):
        """
        Gets all sensors in a survey and optionally returns
        their statuses.
        """
        # Check whether the Survey ID requested is actually
        # an integer.
        if isinstance(survey_id, str):
            if not survey_id.isdigit():
                raise BadOccupEyeRequest

        maps_key = "occupeye:surveys:{}:maps".format(survey_id)
        # Check if we have a list of maps for this survey
        if not self.r.llen(maps_key):
            self._cache_survey_data()

        # If the data still doesn't exist, the map probably doesn't
        # exist, so raise an error.
        if not self.r.llen(maps_key):
            raise BadOccupEyeRequest

        maps = self.r.lrange(
            maps_key,
            0,
            self.r.llen(maps_key) - 1
        )

        survey_data_key = "occupeye:surveys:{}".format(survey_id)
        survey_data = self.r.hgetall(survey_data_key)

        data = {
            "maps": [],
            "survey_id": survey_data["id"],
            "survey_name": survey_data["name"]
        }

        all_survey_sensors_key = (
            "occupeye:surveys:{}:sensors"
        ).format(survey_id)
        # If we do not have the data for each survey's sensor then
        # we should go ahead and cache that.
        if not self.r.exists(all_survey_sensors_key):
            self._cache_survey_sensor_data(survey_id)

        survey_sensors_ids = self.r.lrange(
            all_survey_sensors_key,
            0,
            self.r.llen(all_survey_sensors_key)
        )
        pipeline = self.r.pipeline()

        # Dictionary with the general :data for for every sensor
        # in the survey with no regard for map
        survey_sensors_data = dict()
        for sensor_id in survey_sensors_ids:
            sensor_data_key = (
                "occupeye:surveys:{}:sensors:{}:data"
            ).format(survey_id, sensor_id)
            pipeline.hgetall(sensor_data_key)

        for sensor_data in pipeline.execute():
            survey_sensors_data[sensor_data["hardware_id"]] = sensor_data

        for map_id in maps:
            map_sensors_key = "occupeye:surveys:{}:maps:{}:sensors".format(
                survey_id,
                map_id
            )
            if not self.r.llen(map_sensors_key):
                self._cache_sensors_for_map(survey_id, map_id)

            sensor_hw_ids = self.r.lrange(
                map_sensors_key,
                0,
                self.r.llen(map_sensors_key) - 1
            )

            sensors = OrderedDict()

            # Get sensor properties requests into a pipeline
            # Whilst at it, grab the :data from survey_sensors_data
            for sensor_id in sensor_hw_ids:
                sensor_properties_key = (
                    "occupeye:surveys:{}:maps:{}:sensors:{}:properties"
                ).format(survey_id, map_id, sensor_id)
                pipeline.hgetall(sensor_properties_key)

            # Now execute that pipeline
            for result in pipeline.execute():
                hw_id = result['hardware_id']
                if hw_id in survey_sensors_data:
                    sensors[hw_id] = {**result, **survey_sensors_data[hw_id]}
                else:
                    sensors[hw_id] = result

            # Now do the same thing again if states were requested
            if return_states:
                # All HW sensor state values have the same TTL and are added
                # using a transaction, so we can check just the first sensor
                # HW ID. If we have data on it, we assume we can use the cache.
                # If not, we retrieve all the latest data.
                first_sensor_status_key = (
                    "occupeye:surveys:{}:sensors:{}:status"
                ).format(survey_id, sensor_hw_ids[0])
                if not self.r.hgetall(first_sensor_status_key):
                    self._cache_all_survey_sensor_states(survey_id)

                for sensor_id in sensor_hw_ids:
                    sensor_status_key = (
                         "occupeye:surveys:{}:sensors:{}:status"
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

            map_data = self.r.hgetall(
                "occupeye:surveys:{}:maps:{}".format(survey_id, map_id)
            )
            pipeline.execute()
            map_data["sensors"] = sensors

            data["maps"].append(map_data)

        if return_states:
            max_timestamp_key = (
                "occupeye:surveys:{}:sensors:max_timestamp"
            ).format(survey_id)
            data["most_recent_timestamp"] = self.r.get(max_timestamp_key)

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
            "occupeye:surveys:{}:sensors:max_timestamp"
        ).format(survey_id)

        max_timestamp_cached = self.r.get(max_timestamp_key)
        if max_timestamp_cached:
            return (int(survey_id), max_timestamp_cached)
        else:
            max_timestamp = self._get_survey_sensor_max_timestamp(survey_id)
            self.r.set(max_timestamp_key, max_timestamp)
            return (int(survey_id), max_timestamp)

    def _get_survey_sensors_data_worker(self, survey_id, survey_name, lock, data_dict):
        survey_data = {
            "id": survey_id,
            "name": survey_name,
            "maps": []
        }
        sensors = self.get_survey_sensors(survey_id, True)
        for survey_map in sensors["maps"]:
            map_data = {
                "id": survey_map["id"],
                "name": survey_map["name"],
                "sensors_absent": 0,
                "sensors_occupied": 0,
                "sensors_other": 0
            }
            for hw_id, sensor in survey_map["sensors"].items():
                if "last_trigger_type" in sensor:
                    if sensor["last_trigger_type"] == "Absent":
                        map_data["sensors_absent"] += 1
                    elif sensor["last_trigger_type"] == "Occupied":
                        map_data["sensors_occupied"] += 1
                    else:
                        map_data["sensors_other"] += 1

            survey_data["maps"].append(map_data)
        lock.acquire()
        data_dict[survey_id] = survey_data
        lock.release()

    def get_survey_sensors_summary(self, survey_ids):
        """
        Gets a summary of every survey, map and the sensor counts within them.
        """
        surveys_data = self.get_surveys()

        if survey_ids:
            try:
                survey_ids_list = [int(x) for x in survey_ids.split(',')]
            except ValueError:
                raise BadOccupEyeRequest
        else:
            survey_ids_list = None

        filtered_surveys = []

        if survey_ids_list:
            for survey in surveys_data:
                if survey["id"] in survey_ids_list:
                    filtered_surveys.append(survey)
        else:
            filtered_surveys = surveys_data

        if survey_ids_list:
            if len(filtered_surveys) != len(survey_ids_list):
                raise BadOccupEyeRequest

        lock = Lock()
        threads = []

        manager = Manager()
        sensors_data_dict = manager.dict()

        for survey in filtered_surveys:
            p = Process(
                target=self._get_survey_sensors_data_worker,
                args=(survey["id"], survey["name"], lock, sensors_data_dict, )
            )
            threads.append(p)
            p.start()

        for thread in threads:
            thread.join()

        return sensors_data_dict.values()

    def feed_cache(self):
        """
        Function called by the Django management command to feed the Redis
        cache with as much 24-hour valid information as possible. This
        code should be run at night so that commands during the day are
        quicker.
        It can also be run during the day if the code is updated or we are
        notified of any significant changes to Cad-Cap that require a refresh
        during the day.
        """
        self._cache_survey_data()
        survey_ids = self.r.lrange(
            "occupeye:surveys",
            0,
            self.r.llen("occupeye:surveys") - 1
        )
        # Cache all the latest surveys
        for survey_id in survey_ids:
            # Cache a list of every map in the survey
            self._cache_maps_for_survey(survey_id)
            # Cache the data for every sensor in the survey
            self._cache_survey_sensor_data(survey_id)

            # Get a list of every map in the survey based on the the result of
            # running _cache_maps_for_survey above
            survey_maps_key = "occupeye:surveys:{}:maps".format(
                survey_id
            )
            survey_map_ids = self.r.lrange(
                survey_maps_key,
                0,
                self.r.llen(survey_maps_key) - 1
            )
            # Cache data for every map within every survey
            for survey_map_id in survey_map_ids:
                survey_map = self.r.hgetall(
                    "occupeye:surveys:{}:maps:{}".format(
                        survey_id,
                        survey_map_id
                    )
                )
                # Cache the base64 representation of the raw image
                # for the survey
                image_id = int(survey_map["image_id"])
                self._cache_image(image_id)
                # Cache a list of every sensor in every map
                self._cache_sensors_for_map(survey_id, survey_map_id)

            self._cache_all_survey_sensor_states(survey_id)
