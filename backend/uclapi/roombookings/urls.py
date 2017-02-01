from django.conf.urls import url, include
import roombookings.views

urlpatterns = [
    url(r'^rooms$', roombookings.views.get_rooms),
    url(r'^booking$', roombookings.views.get_bookings),
    url(r'^booking.pagination$', roombookings.views.paginated_result)
]
