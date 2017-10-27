from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pcavailability$', views.get_pc_availability),
]
