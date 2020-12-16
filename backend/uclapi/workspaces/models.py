"""
Models for Workspaces app
"""
from django.db import models
from datetime import datetime


class Sensors(models.Model):
    sensor_id = models.IntegerField()
    survey_id = models.IntegerField()
    hardware_id = models.IntegerField()
    survey_device_id = models.IntegerField()

    def __str__(self):
        return f"Sensors object, {self.sensor_id} @ {self.survey_id}"

    class Meta:
        _DATABASE = 'default'
        unique_together = ('sensor_id', 'survey_id')


class SensorReplacements(models.Model):
    sensor_id = models.IntegerField()
    old_hardware_id = models.IntegerField()
    old_survey_device_id = models.IntegerField()
    old_survey_id = models.IntegerField()
    new_hardware_id = models.IntegerField()
    new_survey_device_id = models.IntegerField()
    new_survey_id = models.IntegerField()
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Sensor replacement object, {self.sensor_id}: {self.datetime}"

    class Meta:
        _DATABASE = 'default'

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
        _DATABASE = 'default'
        unique_together = ('sensor_id', 'survey_id', 'datetime')


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
        _DATABASE = 'default'


class SurveyChanges(models.Model):
    survey_id = models.IntegerField()
    old_name = models.TextField()
    old_start_datetime = models.DateTimeField()
    old_end_datetime = models.DateTimeField()
    old_active = models.BooleanField()
    new_name = models.TextField()
    new_start_datetime = models.DateTimeField()
    new_end_datetime = models.DateTimeField()
    new_active = models.BooleanField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"Survey changes object, {self.survey_id}: {self.datetime}"

    class Meta:
        _DATABASE = 'default'
