from django.conf.urls import url

from dashboard.api_applications import (
    create_app, delete_app, regenerate_app_token, rename_app, set_callback_url,
    update_scopes, number_of_requests, quota_remaining, most_popular_service,
    most_popular_method, users_per_app, users_per_app_by_dept,
    get_apps
)

from . import views, webhook_views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'api/analytics/total$', number_of_requests),
    url(r'api/analytics/quota$', quota_remaining),
    url(r'api/analytics/services$', most_popular_service),
    url(r'api/analytics/methods$', most_popular_method),
    url(r'api/analytics/oauth/total$', users_per_app),
    url(r'api/analytics/oauth/total_by_dept$', users_per_app_by_dept),
    url(r'api/apps/$', get_apps),
    url(r'api/create/$', create_app),
    url(r'api/rename/$', rename_app),
    url(r'api/regen/$', regenerate_app_token),
    url(r'api/delete/$', delete_app),
    url(r'api/setcallbackurl/$', set_callback_url),
    url(r'api/updatescopes/$', update_scopes),
    url(r'^user/login.callback', views.ad_callback),
    url(r'api/webhook/edit/$', webhook_views.edit_webhook),
    url(
        r'api/webhook/refreshsecret/$',
        webhook_views.refresh_verification_secret
    )
]
