from django.conf.urls import url

from dashboard.api_applications import (create_app, delete_app,
                                        regenerate_app_token, rename_app,
                                        set_callback_url, update_scopes)

from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'api/create/$', create_app),
    url(r'api/rename/$', rename_app),
    url(r'api/regen/$', regenerate_app_token),
    url(r'api/delete/$', delete_app),
    url(r'api/setcallbackurl/$', set_callback_url),
    url(r'api/updatescopes/$', update_scopes),
    url(r'^user/login.callback', views.shibboleth_callback)
]
