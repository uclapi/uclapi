from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'authorise/$', views.authorise),
    url(r'shibcallback$', views.shibcallback),
    url(r'token$', views.token),
    url(r'user/allow$', views.userallow),
    url(r'user/deny$', views.userdeny),
    url(r'user/data$', views.userdata)
]
