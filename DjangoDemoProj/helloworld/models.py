# coding: utf-8
from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField('姓名', max_length=32, unique=False, help_text='姓名')
    age = models.IntegerField('年龄', null=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'helloworld'
        db_table = 'person'

class Book(models.Model):
    name = models.CharField('名称', max_length=128, unique=False, help_text='书籍名称')
    writer = models.CharField('作者', max_length=32, unique=False, default='未知', help_text='作者姓名')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'helloworld'
        db_table = 'book'