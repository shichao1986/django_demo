# coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request, name, age):
    return HttpResponse('Hello world! {} is {} year(s) old.'.format(name, age))

def index2(request, name, age):
    return render('helloworld/index.html', dict(name=name, age=age))

def index_render(request, name, age):
    return render('helloworld/index_render.html', dict(name=name, age=age))

def index_old(request, name, age):
    pass

def index3(request, name, age):
    return