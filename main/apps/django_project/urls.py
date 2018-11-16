from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index),
        url(r'^register/$', views.register),
        url(r'^login/$', views.login),
        url(r'^wishes/$', views.wishes, name='wishes'),
        url(r'^wishes/delete/(?P<id>\d+)/$', views.delete),
        url(r'^wishes/new/$', views.new, name='new'),
        url(r'^wishes/new/create/$', views.create, name='create'),
        url(r'^wishes/like/(?P<id>\d+)/$', views.like),
        url(r'^wishes/stats/$', views.stats, name='stats'),
        url(r'^wishes/edit/(?P<id>\d+)/$', views.edit),
        url(r'^wishes/logout/$', views.logout, name='logout'),
        url(r'^wishes/granted/(?P<id>\d+)/$', views.granted, name='granted'),
        url(r'^wishes/edit/(?P<id>\d+)/update/$', views.update),
        ]
