# coding: utf-8

# 本模块自定义数据库查询时的聚合函数

from django.db.models.aggregates import Aggregate

'''
pg中使用group_concat的语法，例如：

SELECT "school"."name", GROUP_CONCAT("person"."name") AS "person_num" FROM "person" LEFT OUTER JOIN
"school" ON ("person"."school_id" = "school"."id") GROUP BY "school"."name" LIMIT 21;
'''

class MyConcat(Aggregate):
    function = 'GROUP_CONCAT'   # postgresql 中的函数名称
    name = 'MyConcat'
    template = '%(function)s(%(expressions)s)'      #  GROUP_CONCAT("person"."name")


'''示例：
>>> from helloworld.my_concat import MyConcat
>>> from helloworld.models import *
>>>
>>> Person.objects.values('school__name').annotate(persons=MyConcat('name'))
2018-12-28 05:47:17,552 django.db.backends DEBUG utils.py [execute 91]: (0.003) SELECT "school"."name",
GROUP_CONCAT("person"."name") AS "persons" FROM "person" LEFT OUTER JOIN "school" ON
("person"."school_id" = "school"."id") GROUP BY "school"."name" LIMIT 21; args=()
<QuerySet [{'school__name': '武汉大学', 'persons': ['程天', '恺恺', '刘一']}, {'school__name': '清华大学', 'persons': ['李四', '张三']}]>

'''