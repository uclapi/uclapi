from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get$', views.get_personal_timetable),
    url(r'^modules$', views.get_modules_timetable),
]
