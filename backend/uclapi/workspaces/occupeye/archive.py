from datetime import datetime, timedelta, timezone
from typing import List

from workspaces.models import Surveys, Historical, Sensors, SensorReplacements, SurveyChanges
from .constants import OccupEyeConstants
from .endpoint import OccupeyeEndpoint, Endpoint

FIRST_OCCUPEYE_INSTALLATION = datetime.strptime("2017-01-01T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z")
MAX_TIME_DELTA = timedelta(days=28)


class OccupEyeArchive:
    def __init__(self, endpoint: Endpoint = None):
        if endpoint is None:
            endpoint = OccupeyeEndpoint()
        self._const = OccupEyeConstants()
        self._endpoint = endpoint

    def reset(self):
        Surveys.objects.all().delete()
        Sensors.objects.all().delete()
        Historical.objects.all().delete()

    def extract_sensor_date(self, dict, prefix):
        dt = datetime.strptime(dict[f"{prefix}Date"] + "t" + dict[f"{prefix}Time"], "%Y-%m-%dt%H:%M")
        return dt.replace(tzinfo=None)

    def refresh_sensors(self):
        new_updates, delta_updates = 0, 0
        all_surveys = self._endpoint.request(self._const.URL_SURVEYS_ALL)
        for survey in all_surveys:
            if not Surveys.objects.filter(survey_id=survey["SurveyID"]).exists():
                new_updates += 1
                start_datetime = self.extract_sensor_date(survey, "Start")
                end_datetime = self.extract_sensor_date(survey, "End")
                new_survey = Surveys.objects.create(survey_id=survey["SurveyID"], name=survey["Name"],
                                                    start_datetime=start_datetime, end_datetime=end_datetime,
                                                    active=survey["Active"], last_updated=FIRST_OCCUPEYE_INSTALLATION)
                SurveyChanges.objects.create(survey=new_survey, name=survey["Name"],
                                             start_datetime=start_datetime, end_datetime=end_datetime,
                                             active=survey["Active"])

            validate = Surveys.objects.get(survey_id=survey["SurveyID"])
            if survey["Name"] != validate.name or self.extract_sensor_date(survey, "Start") != \
                    validate.start_datetime or self.extract_sensor_date(survey, "End") != validate.end_datetime \
                    or survey["Active"] != validate.active:
                delta_updates += 1
                SurveyChanges.objects.create(survey=validate, name=survey["Name"],
                                             start_datetime=self.extract_sensor_date(survey, "Start"),
                                             end_datetime=self.extract_sensor_date(survey, "End"),
                                             active=survey["Active"])

                validate.name = survey["Name"]
                validate.start_datetime = self.extract_sensor_date(survey, "Start")
                validate.end_datetime = self.extract_sensor_date(survey, "End")
                validate.active = survey["Active"]
                validate.save()

        print(f"[+] Added {new_updates} new surveys, updated {delta_updates} surveys")

    @staticmethod
    def time_steps(start: datetime, end: datetime) -> List[datetime]:
        """
        Generates all datetime steps between a start and end datetime with a maximum change
        of MAX_TIME_DELTA
        """
        steps = []
        while start < end:
            steps.append(start)
            start = start + MAX_TIME_DELTA
            if start > end:
                start = end
            steps[-1] = (steps[-1], start)
            start += timedelta(days=1)
        return steps

    def get_current_sensors(self):
        """
        Get all sensors, this is more efficient than using a filter every time as each sensor is verified every
        24 hours.
        """
        self.refresh_sensors()
        current_sensors = list(Sensors.objects.all().values())
        # Convert the list of dictionaries to a dictionary with the sensor_id as the key
        current_sensors = {str(obj["sensor_id"]) + "-" + str(obj["survey_id"]):
                           {k: obj[k] for k in obj if k != "sensor_id"} for obj in current_sensors}
        for key in current_sensors:
            obj = Historical.objects.filter(sensor_id=key.split("-")[0], survey_id=key.split("-")[1]).order_by(
                "-datetime").values("state").first()
            last_value = -1 if obj is None else obj["state"]

            current_sensors[key]["last_value"] = last_value
        return current_sensors

    def validate_sensor(self, sensor, survey, start_date, end_date):
        """
        Every 24 hour period for a single sensor includes a sensor_id, survey_id, hardware_id, and survey_device_id,
        very rarely these will be different to a previous sensor even if they have the same sensor_id and survey_id.
        This function verifies a sensor is the same as the previous detected sensor
        """
        cs_key = str(sensor["SensorID"]) + f"-{survey.survey_id}"

        validate = self.current_sensors[cs_key]
        if sensor["HardwareID"] != validate["hardware_id"] or \
                sensor["SurveyDeviceID"] != validate["survey_device_id"] or \
                survey.survey_id != validate["survey_id"]:
            print("\n      [+] Sensor does not match historical records")
            if survey.survey_id == validate["survey_id"]:
                print("      [+] Sensor in same location")
                print(f"      [+] Updating {validate['hardware_id']} -> {sensor['HardwareID']}")
                print(f"      [+] Updating {validate['survey_device_id']} -> {sensor['SurveyDeviceID']}")
                obj = Sensors.objects.get(sensor_id=sensor["SensorID"])

                time = datetime.strptime(sensor["TriggerDate"], "%Y-%m-%d")
                time = time.replace(tzinfo=timezone.utc)
                SensorReplacements.objects.create(sensor_id=sensor["SensorID"],
                                                  survey_id=validate["survey_id"],
                                                  hardware_id=validate['hardware_id'],
                                                  survey_device_id=validate['survey_device_id'],
                                                  datetime=time)

                obj.hardware_id = sensor["HardwareID"]
                obj.survey_device_id = sensor["SurveyDeviceID"]
                obj.save()
                self.current_sensors[str(sensor["SensorID"]) + "-" + str(survey.survey_id)] = {
                    "hardware_id": sensor["HardwareID"], "survey_device_id": sensor["SurveyDeviceID"],
                    "survey_id": survey.survey_id, "last_value": -1}
            else:
                print(f"      [+] Sensor in different location "
                      f"{validate['survey_id']} -> {survey.survey_id}")
                Sensors.objects.create(sensor_id=sensor["SensorID"], hardware_id=sensor["HardwareID"],
                                       survey_device_id=sensor["SurveyDeviceID"],
                                       survey_id=survey.survey_id)
                self.current_sensors[str(sensor["SensorID"]) + "-" + str(survey.survey_id)] = {
                    "hardware_id": sensor["HardwareID"], "survey_device_id": sensor["SurveyDeviceID"],
                    "survey_id": survey.survey_id, "last_value": -1}

            print(f"   [+] Continuing {start_date} to {end_date} ", end="")

    def update(self):
        self.current_sensors = self.get_current_sensors()

        end_time = datetime.now().replace(microsecond=0, second=0, minute=0, hour=0)
        for survey in Surveys.objects.all():
            print(f"[+] Updating {survey.survey_id} from {survey.last_updated} to {end_time}")
            for step in self.time_steps(survey.last_updated, end_time):
                start_date = step[0].strftime("%Y-%m-%d")
                end_date = step[1].strftime("%Y-%m-%d")

                print(f"   [+] Requesting {start_date} to {end_date} ", end="")
                updates = 0
                sensors = self._endpoint.request(
                    self._const.URL_ARCHIVE.format(start_date, end_date, survey.survey_id))

                # Sensors where the hardware id or survey device id have changed will have two sets of data
                # We want to keep the data with the greatest hardware ID or survey device ID
                unique_sensors = {}
                for key, sensor in enumerate(sensors):
                    unique_key = str(sensor["SensorID"]) + ":" + sensor["TriggerDate"]
                    unique_value = sensor["HardwareID"] + sensor["SurveyDeviceID"]
                    if unique_key in unique_sensors:
                        if unique_value > unique_sensors[unique_key][1]:
                            unique_sensors[unique_key] = (key, unique_value)
                    else:
                        unique_sensors[unique_key] = (key, unique_value)

                filtered_sensors = []
                for _, value in unique_sensors.items():
                    filtered_sensors.append(sensors[value[0]])

                sensors = filtered_sensors
                batch_objects = []

                for sensor in sensors:
                    cs_key = str(sensor["SensorID"]) + f"-{survey.survey_id}"
                    if cs_key in self.current_sensors:
                        self.validate_sensor(sensor, survey, start_date, end_date)
                    else:
                        Sensors.objects.create(sensor_id=sensor["SensorID"], hardware_id=sensor["HardwareID"],
                                               survey_device_id=sensor["SurveyDeviceID"],
                                               survey_id=survey.survey_id)
                        self.current_sensors[str(sensor["SensorID"]) + "-" + str(survey.survey_id)] = {
                            "hardware_id": sensor["HardwareID"], "survey_device_id": sensor["SurveyDeviceID"],
                            "survey_id": survey.survey_id, "last_value": -1}

                    for key, value in sensor.items():
                        if key.startswith("t"):
                            # A few time stamps have None instead of -1
                            if value is None:
                                value = -1
                            if value != self.current_sensors[cs_key]["last_value"]:
                                updates += 1
                                time = datetime.strptime(sensor["TriggerDate"] + key, "%Y-%m-%dt%H%M")
                                time = time.replace(tzinfo=timezone.utc)
                                batch_objects.append(
                                    Historical(sensor_id=sensor["SensorID"], survey_id=survey.survey_id,
                                               datetime=time, state=value))
                                self.current_sensors[cs_key]["last_value"] = value

                # Ideally ignore conflicts would be false but depending on exactly when the archive is run or
                # if the previous run crashed some conflicts may exist.
                Historical.objects.bulk_create(batch_objects, batch_size=65536, ignore_conflicts=True)
                print(f"{updates} updates")

            survey.last_updated = end_time
            survey.save()
