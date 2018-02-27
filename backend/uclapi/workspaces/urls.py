from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^surveys$', views.get_surveys),
     url(r'^image$', views.get_image),
     url(r'^sensors/lastupdated$', views.get_survey_max_timestamp),
     url(r'^sensors/summary$', views.get_survey_sensors_summary),
     url(r'^sensors$', views.get_survey_sensors),
]
