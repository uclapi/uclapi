from django.urls import path

from . import views

urlpatterns = [
    path(r"surveys", views.get_surveys),
    path(r"images/map/live", views.get_live_map),
    path(r"images/map", views.get_map_image),
    path(r"sensors/lastupdated", views.get_survey_max_timestamp),
    path(r"sensors/summary", views.get_survey_sensors_summary),
    path(r"sensors/averages/time", views.get_averages_time),
    path(r"sensors", views.get_survey_sensors),
    path(r"historical/surveys", views.SurveysList.as_view()),
    path(r"historical/sensors", views.SensorsList.as_view()),
    path(r"historical/data", views.HistoricalList.as_view()),
]
