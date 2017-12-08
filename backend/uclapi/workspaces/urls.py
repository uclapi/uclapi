from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^rooms$', views.get_rooms),
     url(r'^image$', views.get_image),
]
