from django.conf.urls import url

import search.views

urlpatterns = [
    url(r'^people$', search.views.people),
]
