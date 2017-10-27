from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^desktop_availability$', views.get_pc_availability),
]
