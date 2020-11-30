from django.urls import path

from . import views

urlpatterns = [
    path('space/locations', views.get_locations),
]
