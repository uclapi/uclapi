from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^personal$', views.get_personal_timetable_endpoint),
    url(r'^bymodule$', views.get_modules_timetable_endpoint),
    url(r'^data/courses$', views.get_department_courses_endpoint),
    url(r'^data/courses/modules$', views.get_course_modules_endpoint),
    url(r'^data/departments$', views.get_departments_endpoint),
    url(r'^data/modules$', views.get_department_modules_endpoint)
]
