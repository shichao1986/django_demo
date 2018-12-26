# coding: utf-8
from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField('名称', max_length=64, unique=True, help_text='学校名称')
    address = models.TextField('地址', default='', help_text='学校地址')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'helloworld'
        db_table = 'school'

class Book(models.Model):
    name = models.CharField('名称', max_length=128, unique=False, help_text='书籍名称')
    writer = models.CharField('作者', max_length=32, unique=False, default='未知', help_text='作者姓名')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'helloworld'
        db_table = 'book'


class Person(models.Model):
    name = models.CharField('姓名', max_length=32, unique=False, help_text='姓名')
    age = models.IntegerField('年龄', null=False, default=0)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, related_name='persons', verbose_name='学校',
                               help_text='指向学校的外键', default=None, null=True, blank=True)
    books = models.ManyToManyField(Book, through='PersonBookRelation', through_fields=('person', 'book'), blank=True,
                                   related_name='person_relations', verbose_name='书籍')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'helloworld'
        db_table = 'person'

class PersonBookRelation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relations', verbose_name='人员',
                               help_text='人员')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='relations', verbose_name='书籍',
                             help_text='书籍')

    def __str__(self):
        return '{}-{}'.format(self.person.name, self.book.name)

    class Meta:
        app_label = 'helloworld'
        db_table = 'person_book_relation'