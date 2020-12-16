from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^surveys$", views.get_surveys),
    url(r"^images/map/live$", views.get_live_map),
    url(r"^images/map$", views.get_map_image),
    url(r"^sensors/lastupdated$", views.get_survey_max_timestamp),
    url(r"^sensors/summary$", views.get_survey_sensors_summary),
    url(r"^sensors/averages/time$", views.get_averages_time),
    url(r"^sensors$", views.get_survey_sensors),
    url(r"^historical/sensor$", views.get_historical_sensor),
    url(r"^historical/survey$", views.get_historical_survey),
    url(r"^historical/list/sensors$", views.get_historical_list_sensors),
    url(r"^historical/list/surveys$", views.get_historical_list_surveys),
    url(r"^historical/takeout", views.get_historical_survey)
]
