from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'add_email$', views.add_email),
    url(r'delete$', views.delete_email)
]
