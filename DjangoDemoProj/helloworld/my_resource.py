# coding: utf-8

from import_export import resources
from .models import *

'''
resource的写法如下
Meta中的fields指导出哪些列，可以用外键的__方法
Meta中的export_order指导出列的顺序
get_export_headers是指excel的表头
dehydrate_%filed%是指你可以对某一列做一些定制，同类似serializer里面的SerializerMethodField，但是只能是model上存在的%filed%才可以
'''

class PersonResource(resources.ModelResource):
    def dehydrate_books(self, obj):
        return str(obj.books) if obj.books else '[]'

    def get_export_headers(self):
        return ['姓名', '年龄', '爱好', '自我介绍', '学校', '书籍']

    class Meta:
        model = Person
        fields = ('name', 'age', 'favorates',
                  'introduce', 'school__name', 'books')
        export_order = ('name', 'age', 'favorates',
                  'introduce', 'school__name', 'books')