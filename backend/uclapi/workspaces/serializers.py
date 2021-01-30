from rest_framework import serializers


class SurveysSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    name = serializers.StringRelatedField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    active = serializers.BooleanField()
    last_updated = serializers.DateTimeField()


class SensorsSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    sensor_id = serializers.IntegerField()
    hardware_id = serializers.IntegerField()
    survey_device_id = serializers.IntegerField()


class HistoricalSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    sensor_id = serializers.IntegerField()
    datetime = serializers.DateTimeField()
    state = serializers.IntegerField()
