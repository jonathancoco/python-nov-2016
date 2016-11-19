from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_course', views.add_course),
    url(r'^remove_course/(?P<id>\d+)$', views.remove_course),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^edit_course/(?P<id>\d+)$', views.edit_course),
    url(r'^save_course/(?P<id>\d+)$', views.save_course),
    url(r'^view_comments/(?P<id>\d+)$', views.view_comments),
    url(r'^add_comment/(?P<id>\d+)$', views.add_comment)
]
