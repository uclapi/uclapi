from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'authorise/$', views.authorise),
    url(r'shibcallback$', views.shibcallback)
]