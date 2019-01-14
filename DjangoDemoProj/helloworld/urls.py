# coding: utf-8

from django.conf.urls import url
from . import views as hello_views
from rest_framework import permissions

urlpatterns = [
    url(r'^hello/index/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index, name='hello'),
    url(r'^hello/index2/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index2, name='hello2'),
    url(r'^hello/index_render/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index_render, name='hello_render'),
    url(r'^hello/session_test', hello_views.sessiontest, name='session_test'),
    url(r'^hello/rest/persons', hello_views.PersonView.as_view()),
    url(r'^hello/rest/persons2', hello_views.PersonViewSet.as_view({'get':'list'})),
]