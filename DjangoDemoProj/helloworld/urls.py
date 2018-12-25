# coding: utf-8

from django.conf.urls import url
from . import views as hello_views

urlpatterns = [
    url(r'^hello/index/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index, name='hello'),
    url(r'^hello/index2/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index2, name='hello2'),
    url(r'^hello/index_render/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index_render, name='hello_render'),
]