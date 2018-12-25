# coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request, name, age):
    return HttpResponse('Hello world! {} is {} year(s) old.'.format(name, age))