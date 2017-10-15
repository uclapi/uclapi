from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^personal$', views.get_personal_timetable),
    url(r'^bymodule$', views.get_modules_timetable),
    url(r'^data/courses$', views.get_department_courses),
    url(r'^data/course/modules$', views.get_course_modules),
    url(r'^data/departments$', views.get_departments),
    url(r'^data/modules$', views.get_department_modules)
]
