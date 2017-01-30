from django.conf.urls import url, include
from dashboard.views import dashboard 
from dashboard.api_applications import create_app, rename_app, regenerate_app_token, delete_app

urlpatterns = [
    url(r'/$', dashboard),
    url(r'api/create/$', create_app),
    url(r'api/rename/$', rename_app),
    url(r'api/regen/$', regenerate_app_token),
    url(r'api/delete/$', delete_app)
]
