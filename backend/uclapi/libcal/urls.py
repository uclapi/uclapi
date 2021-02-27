from django.urls import path

from . import views

urlpatterns = [
    path('space/locations', views.get_locations),
    path('space/form', views.get_form),
    path('space/question', views.get_question),
    path('space/categories', views.get_categories),
    path('space/category', views.get_category),
    path('space/item', views.get_item),
]
