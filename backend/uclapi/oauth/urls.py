from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'authorise/$', views.authorise),
    url(r'adcallback', views.adcallback),
    url(r'token$', views.token),
    url(r'tokens/scopes$', views.scope_map),
    url(r'tokens/test$', views.token_test),
    url(r'user/allow$', views.userallow),
    url(r'user/deny$', views.userdeny),
    url(r'user/data$', views.userdata),
    url(r'user/studentnumber$', views.get_student_number),
    url(r'deauthorise$', views.deauthorise_app),
    url(r'user/settings$', views.get_settings)
]
