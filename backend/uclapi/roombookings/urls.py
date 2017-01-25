from django.conf.urls import url, include
import roombookings.views

urlpatterns = [
    url(r'^get', roombookings.views.get_rooms),
]
