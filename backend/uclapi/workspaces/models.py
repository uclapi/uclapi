"""
Models for Workspaces app
"""
from datetime import datetime

from django.db import models


class Sensors(models.Model):
    sensor_id = models.IntegerField()
    survey_id = models.IntegerField()
    hardware_id = models.IntegerField()
    survey_device_id = models.IntegerField()

    def __str__(self):
        return f"Sensors object, {self.sensor_id} @ {self.survey_id}"

    class Meta:
        _DATABASE = "default"
        constraints = [
            models.UniqueConstraint(fields=["sensor_id", "survey_id"], name="sensors_composite_primary_key")
        ]


# Stores the previous values at sensor replacement, for example if hardware_id changed from 1 to 2 on 2020-01-01
# then hardware_id = 1 and datetime = 2020-01-01 would be stored. This is to prevent storing thousands of sensors
# which will never change.
class SensorReplacements(models.Model):
    sensor_id = models.IntegerField()
    hardware_id = models.IntegerField()
    survey_device_id = models.IntegerField()
    survey_id = models.IntegerField()
    # The datetime when the sensor was replaced
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Sensor replacement object, {self.sensor_id}: {self.datetime}"

    class Meta:
        _DATABASE = "default"


# OccupEye ruined a great algorithm because they allow sensors to exist
# in two different locations at exactly the same time, therefore we need
# both sensor_id and survey_id
class Historical(models.Model):
    sensor_id = models.IntegerField()
    survey_id = models.IntegerField()
    datetime = models.DateTimeField()
    state = models.IntegerField()

    def __str__(self):
        return f"Historical object, {self.sensor_id}, {self.survey_id}, {self.datetime}: {self.state}"

    class Meta:
        _DATABASE = "default"
        constraints = [
            models.UniqueConstraint(fields=["sensor_id", "survey_id", "datetime"],
                                    name="historical_composite_primary_key")
        ]


class Surveys(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    active = models.BooleanField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"Survey object, {self.survey_id}: {self.name} from {self.last_updated}"

    class Meta:
        _DATABASE = "default"


# Stores the current value at survey change, for example if active changed from false to true on 2020-01-01
# then active = true and datetime = 2020-01-01 would be stored. Unlike Sensor Replacements, survey changes happen
# frequently
class SurveyChanges(models.Model):
    survey = models.ForeignKey(to=Surveys, on_delete=models.CASCADE)
    name = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    active = models.BooleanField()
    # The datetime when the survey was changed
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"Survey changes object, {self.survey_id}: {self.datetime}"

    class Meta:
        _DATABASE = "default"
