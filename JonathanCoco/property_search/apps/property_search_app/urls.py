from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^view_search$', views.view_search),
    url(r'^contact$', views.contact),
    url(r'^view_login$', views.view_login),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^logout$', views.logout),
    url(r'^search$', views.search),
    url(r'^view_property/(?P<id>\d+)$', views.view_property),
    url(r'^view_search_results/(?P<id>\d+)$', views.view_search_results),
    url(r'^sort_list/(?P<sort_option>\w+)$', views.sort_list)
]
