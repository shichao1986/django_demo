# coding: utf-8

from django.conf.urls import url
from . import views as hello_views

urlpatterns = [
    url(r'^hello/index/(?P<name>[\w]+/(?P<age>[\d]+))', hello_views.index),
]