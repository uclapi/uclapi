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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from common.views import ping_view
from oauth.views import logout
from dashboard.views import DevelopmentNextjsProxyView
from settings import DEBUG

app_name = "uclapi"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/api/', include('dashboard.urls')),
    path('logout/', logout),
    path('roombookings/', include('roombookings.urls')),
    path('oauth/', include('oauth.urls')),
    path('timetable/', include('timetable.urls')),
    path('search/', include('search.urls')),
    path('resources/', include('resources.urls')),
    path('workspaces/', include('workspaces.urls')),
    path('libcal/', include('libcal.urls')),
    path('ping/', ping_view),
]

# In development mode, use Django to proxy all other routes to the next.js frontend
# In production, Traefik handles this for us (prevents load on Django)
if DEBUG:
    urlpatterns.append(
        url('^(?P<path>.*)$', DevelopmentNextjsProxyView.as_view()),
    )
