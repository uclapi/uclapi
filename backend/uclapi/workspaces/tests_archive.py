import json
import os
from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from freezegun import freeze_time

from .models import Surveys, Historical, Sensors, SensorReplacements, SurveyChanges
from .occupeye.api import OccupEyeApi
from .occupeye.archive import OccupEyeArchive
from .occupeye.endpoint import TestEndpoint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@freeze_time("2020-02-01")
class OccupEyeArchiveTestCase(TestCase):

    @patch("workspaces.occupeye.archive.FIRST_OCCUPEYE_INSTALLATION",
           datetime.strptime("2020-01-01T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z"))
    @patch("workspaces.occupeye.archive.MAX_TIME_DELTA", timedelta(days=7))
    def setUp(self):
        with open(os.path.join(__location__, "tests_archive_cache.json"), encoding="utf-8") as f:
            self.archive = OccupEyeArchive(endpoint=TestEndpoint(json.load(f)))
        self.archive.reset()

        self.assertEqual(Surveys.objects.count(), 0)
        self.assertEqual(Historical.objects.count(), 0)
        self.assertEqual(Sensors.objects.count(), 0)

        self.archive.update()

    def assert_historical_timestamp(self, sensor_id, dt_str, state):
        hist = Historical.objects.filter(sensor_id=sensor_id,
                                         datetime=datetime.strptime(dt_str, "%Y-%m-%dT%H:%M"))
        self.assertEqual(hist.count(), 1)
        self.assertEqual(hist.first().state, state)

    def test_survey(self):
        self.assertEqual(Surveys.objects.count(), 1)
        self.assertEqual(Sensors.objects.count(), 10)
        self.assertDictEqual(Surveys.objects.filter(survey_id=72).values()[0],
                             {"active": True, "end_datetime": datetime(2030, 12, 31, 20, 0),
                              "last_updated": datetime(2020, 2, 1, 0, 0), "name": "Bedford Way LG16",
                              "start_datetime": datetime(2019, 7, 6, 8, 0), "survey_id": 72})
        sensors = Sensors.objects.filter(survey_id=72).values()
        exp_sensors = [{"sensor_id": 20664008, "survey_id": 72, "hardware_id": 664008, "survey_device_id": 14767},
                       {"sensor_id": 20664006, "survey_id": 72, "hardware_id": 664006, "survey_device_id": 14765},
                       {"sensor_id": 20664003, "survey_id": 72, "hardware_id": 664003, "survey_device_id": 14762},
                       {"sensor_id": 20664004, "survey_id": 72, "hardware_id": 664004, "survey_device_id": 14763},
                       {"sensor_id": 20664002, "survey_id": 72, "hardware_id": 664002, "survey_device_id": 14761},
                       {"sensor_id": 20664010, "survey_id": 72, "hardware_id": 664010, "survey_device_id": 14769},
                       {"sensor_id": 20664001, "survey_id": 72, "hardware_id": 664001, "survey_device_id": 14760},
                       {"sensor_id": 20664005, "survey_id": 72, "hardware_id": 664005, "survey_device_id": 14764},
                       {"sensor_id": 20664009, "survey_id": 72, "hardware_id": 664009, "survey_device_id": 14768},
                       {"sensor_id": 20664007, "survey_id": 72, "hardware_id": 664007, "survey_device_id": 14766}]
        for sensor, exp_sensor in zip(sensors, exp_sensors):
            del sensor["id"]
            self.assertDictEqual(sensor, exp_sensor)

    def test_survey_initial(self):
        self.maxDiff = None
        survey_change = SurveyChanges.objects.all().values()
        self.assertEqual(len(survey_change), 1)
        sensor_replacement = survey_change[0]

        del sensor_replacement["id"]
        del sensor_replacement["datetime"]
        self.assertDictEqual(sensor_replacement, {"new_active": True,
                                                  "new_end_datetime": datetime(2030, 12, 31, 20, 0),
                                                  "new_name": "Bedford Way LG16",
                                                  "new_start_datetime": datetime(2019, 7, 6, 8, 0),
                                                  "old_active": None,
                                                  "old_end_datetime": None,
                                                  "old_name": None,
                                                  "old_start_datetime": None,
                                                  "survey_id": 72})

    def test_historical_start(self):
        for sensor in Sensors.objects.filter(survey_id=72):
            hist = Historical.objects.filter(survey_id=72, sensor_id=sensor.sensor_id).order_by("datetime").first()
            self.assertEqual(hist.datetime, datetime.strptime("2020-01-09", "%Y-%m-%d"))
            self.assertEqual(hist.state, 0)

    # Manually tests a few random data points in total there are 229 updates
    def test_historical_random(self):
        self.maxDiff = None

        # Single point in time
        self.assert_historical_timestamp(20664004, "2020-01-19T01:20", 1)
        self.assert_historical_timestamp(20664004, "2020-01-19T01:30", 0)

        # Overlap between days
        self.assert_historical_timestamp(20664002, "2020-01-09T23:40", 1)
        self.assert_historical_timestamp(20664002, "2020-01-10T00:30", 0)

        # Overlap between collection periods
        self.assert_historical_timestamp(20664009, "2020-01-16T23:30", 1)
        self.assert_historical_timestamp(20664009, "2020-01-17T00:40", -1)
        self.assert_historical_timestamp(20664009, "2020-01-17T00:50", 0)

    def tearDown(self):
        self.archive.reset()
        SensorReplacements.objects.all().delete()
        SurveyChanges.objects.all().delete()


@patch("workspaces.occupeye.archive.FIRST_OCCUPEYE_INSTALLATION",
       datetime.strptime("2020-01-01T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z"))
@patch("workspaces.occupeye.archive.MAX_TIME_DELTA", timedelta(days=1))
class OccupEyeArchiveEdgeTestCase(TestCase):

    def run_update(self, data, reset=True):
        self.archive = OccupEyeArchive(endpoint=TestEndpoint(data))
        if reset:
            self.archive.reset()
        self.archive.update()

    @freeze_time("2020-01-02")
    def test_sensor_replacement(self):
        with open(os.path.join(__location__, "tests_archive_edge_cache.json"), encoding="utf-8") as f:
            self.run_update(json.load(f))
        sensor_replacement = SensorReplacements.objects.all().values()
        self.assertEqual(len(sensor_replacement), 1)
        sensor_replacement = sensor_replacement[0]

        del sensor_replacement["id"]
        self.assertDictEqual(sensor_replacement, {"datetime": datetime(2020, 1, 2, 0, 0),
                                                  "new_hardware_id": 109004,
                                                  "new_survey_device_id": 1039,
                                                  "new_survey_id": 10,
                                                  "old_hardware_id": 109006,
                                                  "old_survey_device_id": 1039,
                                                  "old_survey_id": 10,
                                                  "sensor_id": 10629006})

    def test_survey_change(self):
        self.maxDiff = None
        with freeze_time("2020-01-02"):
            with open(os.path.join(__location__, "tests_archive_edge_cache.json"), encoding="utf-8") as f:
                self.run_update(json.load(f))
        with freeze_time("2020-01-04"):
            with open(os.path.join(__location__, "tests_archive_edge_survey_cache.json"), encoding="utf-8") as f:
                self.run_update(json.load(f), reset=False)

        survey_change = SurveyChanges.objects.all().values()
        self.assertEqual(len(survey_change), 2)
        sensor_replacement = survey_change[1]

        del sensor_replacement["id"]
        del sensor_replacement["datetime"]
        self.assertDictEqual(sensor_replacement, {"new_active": True,
                                                  "new_end_datetime": datetime(2050, 1, 1, 15, 0),
                                                  "new_name": "Replacement Room 2",
                                                  "new_start_datetime": datetime(2010, 1, 1, 9, 0),
                                                  "old_active": True,
                                                  "old_end_datetime": datetime(2030, 1, 1, 15, 0),
                                                  "old_name": "Replacement Room",
                                                  "old_start_datetime": datetime(2010, 1, 1, 9, 0),
                                                  "survey_id": 10})

    def tearDown(self):
        Surveys.objects.all().delete()
        Sensors.objects.all().delete()
        Historical.objects.all().delete()
        SensorReplacements.objects.all().delete()
        SurveyChanges.objects.all().delete()


@freeze_time("2020-02-01")
class OccupEyeArchiveApiTestCase(TestCase):

    @patch("workspaces.occupeye.archive.FIRST_OCCUPEYE_INSTALLATION",
           datetime.strptime("2020-01-01T00:00:00+0000", "%Y-%m-%dT%H:%M:%S%z"))
    @patch("workspaces.occupeye.archive.MAX_TIME_DELTA", timedelta(days=7))
    def setUp(self):
        with open(os.path.join(__location__, "tests_archive_cache.json"), encoding="utf-8") as f:
            self.archive = OccupEyeArchive(endpoint=TestEndpoint(json.load(f)))
        self.archive.reset()
        self.archive.update()
        self.api = OccupEyeApi()

    def test_get_historical_sensor(self):
        start_time = datetime.strptime("2020-01-15T13:00", "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime("2020-01-15T14:00", "%Y-%m-%dT%H:%M")
        with_delta = self.api.get_historical_sensor(72, 20664001, start_time, end_time)
        self.assertDictEqual(with_delta, {'2020-01-15T13:10:00': 1, '2020-01-15T13:20:00': 0, '2020-01-15T13:50:00': 1,
                                          '2020-01-15T14:00:00': 0})

        without_delta = self.api.get_historical_sensor(72, 20664001, start_time, end_time, delta=False)
        self.assertDictEqual(without_delta,
                             {'2020-01-15T13:00:00': 0, '2020-01-15T13:10:00': 1, '2020-01-15T13:20:00': 0,
                              '2020-01-15T13:30:00': 0, '2020-01-15T13:40:00': 0, '2020-01-15T13:50:00': 1,
                              '2020-01-15T14:00:00': 0})

    def test_get_historical_survey_sensors(self):
        sensors = self.api.get_historical_survey_sensors(72)
        self.assertListEqual(sensors,
                             [20664008, 20664006, 20664003, 20664004, 20664002, 20664010, 20664001, 20664005, 20664009,
                              20664007])

    def test_get_historical_survey(self):
        start_time = datetime.strptime("2020-01-10T00:00", "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime("2020-01-12T00:00", "%Y-%m-%dT%H:%M")
        surveys = self.api.get_historical_survey(72, start_time, end_time)
        self.assertDictEqual(surveys, {20664008: {}, 20664006: {}, 20664003: {}, 20664004: {},
                                       20664002: {'2020-01-10T00:30:00': 0}, 20664010: {},
                                       20664001: {'2020-01-10T21:40:00': 1, '2020-01-10T21:50:00': 0}, 20664005: {},
                                       20664009: {}, 20664007: {}})

    def test_get_historical_list_sensors(self):
        sensors = self.api.get_historical_list_sensors(72)
        self.assertDictEqual(sensors,
                             {"survey_id": 72, "name": "Bedford Way LG16", "start": datetime(2019, 7, 6, 8, 0),
                              "end": datetime(2030, 12, 31, 20, 0), "active": True,
                              "sensors": [{"sensor_id": 20664008, "hardware_id": 664008, "survey_device_id": 14767},
                                          {"sensor_id": 20664006, "hardware_id": 664006, "survey_device_id": 14765},
                                          {"sensor_id": 20664003, "hardware_id": 664003, "survey_device_id": 14762},
                                          {"sensor_id": 20664004, "hardware_id": 664004, "survey_device_id": 14763},
                                          {"sensor_id": 20664002, "hardware_id": 664002, "survey_device_id": 14761},
                                          {"sensor_id": 20664010, "hardware_id": 664010, "survey_device_id": 14769},
                                          {"sensor_id": 20664001, "hardware_id": 664001, "survey_device_id": 14760},
                                          {"sensor_id": 20664005, "hardware_id": 664005, "survey_device_id": 14764},
                                          {"sensor_id": 20664009, "hardware_id": 664009, "survey_device_id": 14768},
                                          {"sensor_id": 20664007, "hardware_id": 664007, "survey_device_id": 14766}],
                              "last_updated": datetime(2020, 2, 1, 0, 0)})

    def test_get_historical_list_surveys(self):
        surveys = self.api.get_historical_list_surveys()
        self.assertEqual(len(surveys), 1)
        self.assertDictEqual(surveys[0],
                             {"survey_id": 72, "name": "Bedford Way LG16", "start": datetime(2019, 7, 6, 8, 0),
                              "end": datetime(2030, 12, 31, 20, 0), "active": True})
