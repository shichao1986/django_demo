# coding: utf-8

from django.conf.urls import url
from . import views as hello_views
from rest_framework import permissions

urlpatterns = [
    url(r'^hello/index/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index, name='hello'),
    url(r'^hello/index2/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index2, name='hello2'),
    url(r'^hello/index_render/(?P<name>[\w]+)/(?P<age>[\d]+)', hello_views.index_render, name='hello_render'),
    url(r'^hello/session_test', hello_views.sessiontest, name='session_test'),
    # 下边两个url在使用正则匹配的情况下，如果没有加末尾的‘/’则会都匹配到第一个url，所以注意
    # url的匹配规则，不要重复！！！
    url(r'^hello/rest/persons/', hello_views.PersonView.as_view(), name='hello_rest'),
    url(r'^hello/rest/persons2/', hello_views.PersonViewSet.as_view({'get':'list', 'post':'create'}), name='hello_rest2'),
    url(r'^hello/rest/persons3/',
        hello_views.PersonViewSetMethod.as_view({'get': 'list'}, permission_classes=(permissions.AllowAny, )),
        name='hello_rest3'),
]