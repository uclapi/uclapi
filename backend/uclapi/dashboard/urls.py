from django.conf.urls import url, include
from dashboard.views import dashboard, get_started
from dashboard.api_applications import create_app, rename_app, regenerate_app_token, delete_app
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'get_started/$', get_started),
    url(r'api/create/$', create_app),
    url(r'api/rename/$', rename_app),
    url(r'api/regen/$', regenerate_app_token),
    url(r'api/delete/$', delete_app),
    url(r'^user/login.callback', views.shibboleth_callback)
]
