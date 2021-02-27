from django.urls import path

from . import views

urlpatterns = [
    path('space/locations', views.get_locations),
    path('space/form', views.get_form),
    path('space/question', views.get_question),
    path('space/categories', views.get_categories),
    path('space/category', views.get_category),
    path('space/item', views.get_item),
    path('space/nickname', views.get_nickname),
    path('space/utilization', views.get_utilization),
    path('space/seat', views.get_seat),
    path('space/seats', views.get_seats),
    path('space/zone', views.get_zone),
    path('space/zones', views.get_zones),
    path('space/bookings', views.get_bookings),
    path('space/personal_bookings', views.get_personal_bookings),
    path('space/reserve', views.reserve)
]
