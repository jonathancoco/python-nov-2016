from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^products$', views.index),
    url(r'^products/new$', views.new),
    url(r'^products/(?P<id>\d+)/edit$', views.edit),
    url(r'^products/(?P<id>\d+)/delete$', views.delete),
    url(r'^products/(?P<id>\d+)$', views.show),
]
