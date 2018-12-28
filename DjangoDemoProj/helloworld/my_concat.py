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