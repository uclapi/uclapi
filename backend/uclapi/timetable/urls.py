from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_timetable$', views.get_personal_timetable),
    url(r'^module_timeatable$', views.get_modules_timetable),
]
