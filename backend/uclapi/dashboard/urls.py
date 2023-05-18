from django.urls import path

from dashboard.api_applications import (
    create_app, delete_app, regenerate_app_token, rename_app, set_callback_url,
    update_scopes, number_of_requests, quota_remaining, most_popular_service,
    most_popular_method, users_per_app, users_per_app_by_dept,
    get_apps, accept_aup
)

from . import views, webhook_views

urlpatterns = [
    path('analytics/total', number_of_requests),
    path('analytics/quota', quota_remaining),
    path('analytics/services', most_popular_service),
    path('analytics/methods', most_popular_method),
    path('analytics/oauth/total', users_per_app),
    path('analytics/oauth/total_by_dept', users_per_app_by_dept),
    path('apps', get_apps),
    path('create', create_app),
    path('accept-aup', accept_aup),
    path('rename', rename_app),
    path('regen', regenerate_app_token),
    path('delete', delete_app),
    path('setcallbackurl', set_callback_url),
    path('updatescopes', update_scopes),
    path('webhook/edit', webhook_views.edit_webhook),
    path('webhook/refreshsecret',
        webhook_views.refresh_verification_secret
    ),
]
