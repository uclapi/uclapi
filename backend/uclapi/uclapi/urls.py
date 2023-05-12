"""uclapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from dashboard.views import (
    documentation,
    home,
    about,
    warning,
    error_404_view,
    error_500_view,
    custom_page_not_found
)
from common.views import ping_view
from oauth.views import settings, settings_ad_callback, logout
from marketplace.views import marketplace

app_name = "uclapi"

handler404 = error_404_view
handler500 = error_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('docs/', documentation),
    path('about/', about),
    path('settings/', settings),
    path('settings/user/login.callback', settings_ad_callback),
    path('logout/', logout),
    path('warning/', warning),
    path('marketplace/', marketplace),
    path('marketplace/<id>/', marketplace),
    path('roombookings/', include('roombookings.urls')),
    path('oauth/', include('oauth.urls')),
    path('timetable/', include('timetable.urls')),
    path('search/', include('search.urls')),
    path('resources/', include('resources.urls')),
    path('workspaces/', include('workspaces.urls')),
    path('libcal/', include('libcal.urls')),
    path('ping/', ping_view),
    path('', home),
    path('404/', custom_page_not_found),
    path('500/', error_500_view)
]
