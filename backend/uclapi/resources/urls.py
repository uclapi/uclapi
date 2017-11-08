from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^desktops$', views.get_pc_availability),
]
