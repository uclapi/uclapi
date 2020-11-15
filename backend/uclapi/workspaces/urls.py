from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^surveys$", views.get_surveys),
    url(r"^images/map/live$", views.get_live_map),
    url(r"^images/map$", views.get_map_image),
    url(r"^sensors/lastupdated$", views.get_survey_max_timestamp),
    url(r"^sensors/summary$", views.get_survey_sensors_summary),
    url(r"^sensors/averages/time$", views.get_historical_time_data),
    url(r"^sensors$", views.get_survey_sensors),
]
