from django.conf.urls import url, include
import roombookings.views

urlpatterns = [
    url(r'^rooms$', roombookings.views.get_rooms),
    url(r'^bookings$', roombookings.views.get_bookings),
    url(r'^equipment$', roombookings.views.get_equipment),
]
