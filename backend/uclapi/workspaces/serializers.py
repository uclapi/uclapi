from rest_framework import serializers

from workspaces.models import Surveys, Sensors, Historical


class SurveysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surveys
        fields = ["survey_id", "name", "start_datetime", "end_datetime", "active", "last_updated"]


class SensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = ["survey_id", "sensor_id", "hardware_id", "survey_device_id"]


class HistoricalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical
        fields = ["sensor_id", "datetime", "state"]
