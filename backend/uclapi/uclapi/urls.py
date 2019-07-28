"""uclapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dashboard.views import documentation, home
from marketplace.views import marketplace

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^docs', documentation),
    url(r'^marketplace', marketplace),
    url(r'^roombookings/', include('roombookings.urls')),
    url(r'^oauth/', include('oauth.urls')),
    url(r'^timetable/', include('timetable.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^workspaces/', include('workspaces.urls')),
    url(r'^$', home),
]
