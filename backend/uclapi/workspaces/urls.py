from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^rooms$', views.get_rooms),
     url(r'^image$', views.get_image),
     url(r'^sensors/last_updated$', views.get_survey_max_timestamp),
     url(r'^sensors$', views.get_survey_sensors),
]
