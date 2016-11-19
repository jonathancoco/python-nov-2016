from django.conf.urls import url
from  . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^add_book_review$', views.add_book_review),
    url(r'^book_reviews/(?P<id>\d+)$', views.book_reviews),
    url(r'^add_review/(?P<id>\d+)$', views.add_review),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review),
    url(r'^user/(?P<id>\d+)$', views.user)
]
