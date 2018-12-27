# coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request, name, age):
    return HttpResponse('Hello world! {} is {} year(s) old.'.format(name, age))

def index2(request, name, age):
    return render(request, 'helloworld/index.html', dict(name=name, age=age))

def index_render(request, name, age):
    return render(request, 'helloworld/index_render.html', dict(name=name, age=age))

def index_old(request, name, age):
    pass

def index3(request, name, age):
    return



# django queryset 操作方法
# 聚合
'''
聚合表时需要明确最终显示的列一共有几列，例如显示 col1  col2  col3   则 这3列或者是被聚合的
或者是需要group by的，一般情况下相同值的列为group_by的，不相同的需要给出聚合方式
如下例中'school__name','person_num'是最终显示的列，则school__name 为group_by，
person_num 给出了聚合方式
Person.objects.all().values('school__name').annotate(person_num=Count('name')).values('school__name','person_num')

另外，django支持的聚合方式有'Avg'(求平均), 'Count'（计数）, 'Max'（最大）, 'Min'（最小）, 'StdDev'（标准差）,
 'Sum'（求和）, 'Variance'（方差）,见django.db.models.aggregates中的定义

'''