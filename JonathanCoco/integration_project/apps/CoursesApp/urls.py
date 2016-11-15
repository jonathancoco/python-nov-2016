from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^add_course', views.add_course, name='add_course'),
    url(r'^remove_course/(?P<id>\d+)$', views.remove_course, name='remove_course'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete_course'),
    url(r'^edit_course/(?P<id>\d+)$', views.edit_course, name='edit_course'),
    url(r'^save_course/(?P<id>\d+)$', views.save_course, name='save_course'),
    url(r'^view_comments/(?P<id>\d+)$', views.view_comments, name='view_comments'),
    url(r'^add_comment/(?P<id>\d+)$', views.add_comment, name='add_comment'),
    url(r'^view_user_courses$', views.view_user_courses, name='view_user_courses'),
    url(r'^add_user_course$', views.add_user_course, name="add_user_course"),
    url(r'^delete_user_course/(?P<id>\d+)$', views.delete_user_course, name="delete_user_course")
]
