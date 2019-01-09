# coding: utf-8

from django.contrib.auth.decorators import login_required
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

@login_required
def sessiontest(request):
    se = request.session
    # session example
    se['username'] = request.user.username
    return HttpResponse('session test')



# django queryset 操作方法
# 查询
# select_related，字表查询一次获得父表的信息
'''
由于queryset的惰性评估机制，只有在使用到它的时候才会去查询数据库，例如
qset = Person.objects.all()     此时还没有对数据库进行查询
p1 = qset[0]        此时才对数据库执行查询操作
在setting.py中重定义名称为django.db.backends 的logger，设置打印级别为DEBUG，在settings.py 的debug开关打开时
 我们能看到数据库sql语句的执行
schoolname = p1.school.name       此时会再此查询school的信息，事实上可以在第一次查询时直接返回相关school信息
使用select_related

qset = Person.objects.all().select_related('school')
p1 = qset[0]
schoolname = p1.school.name     此时不会查询数据库了

'''
# prefetch_related，父表查询两次，获得所有子表信息
'''
>>> pp = Person.objects.all()
>>> for p in pp:
...     print(p.name, p.books.all())
...
2018-12-27 09:35:32,708 django.db.backends DEBUG utils.py [execute 91]: (0.001) SELECT "person"."id", "person"."name", "person"."age", "person"."school_id" FROM "person"; args=()
2018-12-27 09:35:32,710 django.db.backends DEBUG utils.py [execute 91]: (0.001) SELECT "book"."id", "book"."name", "book"."writer" FROM "book" INNER JOIN "person_book_relation" ON ("book"."id" = "person_book_relation"."book_id") WHERE "person_book_relation"."person_id" = 1 LIMIT 21; args=(1,)
张三 <QuerySet [<Book: 笑傲江湖>, <Book: 绝代双骄>]>
2018-12-27 09:35:32,713 django.db.backends DEBUG utils.py [execute 91]: (0.001) SELECT "book"."id", "book"."name", "book"."writer" FROM "book" INNER JOIN "person_book_relation" ON ("book"."id" = "person_book_relation"."book_id") WHERE "person_book_relation"."person_id" = 2 LIMIT 21; args=(2,)
李四 <QuerySet [<Book: 射雕英雄传>, <Book: 笑傲江湖>]>
>>>
>>>
>>>
>>> pp = Person.objects.all().prefetch_related('books')
>>> for p in pp:
...     print(p.name, p.books.all())
...
2018-12-27 09:37:59,940 django.db.backends DEBUG utils.py [execute 91]: (0.000) SELECT "person"."id", "person"."name", "person"."age", "person"."school_id" FROM "person"; args=()
2018-12-27 09:37:59,941 django.db.backends DEBUG utils.py [execute 91]: (0.000) SELECT ("person_book_relation"."person_id") AS "_prefetch_related_val_person_id", "book"."id", "book"."name", "book"."writer" FROM "book" INNER JOIN "person_book_relation" ON ("book"."id" = "person_book_relation"."book_id") WHERE "person_book_relation"."person_id" IN (1, 2); args=(1, 2)
张三 <QuerySet [<Book: 笑傲江湖>, <Book: 绝代双骄>]>
李四 <QuerySet [<Book: 射雕英雄传>, <Book: 笑傲江湖>]>

需要注意的是：pp为queryset，如果直接使用pp[0]，pp[1]，则每次都会进行sql查询，所以需要直接将queryset执行并存入pp中
后续才会不再查询，例子中的方法是给出的一种合法用法

'''

# 聚合
'''
聚合表时需要明确最终显示的列一共有几列，例如显示 col1  col2  col3   则 这3列或者是被聚合的
或者是需要group by的，一般情况下相同值的列为group_by的，不相同的需要给出聚合方式
如下例中'school__name','person_num'是最终显示的列，则school__name 为group_by，
person_num 给出了聚合方式
Person.objects.all().values('school__name').annotate(person_num=Count('name'))

另外，django支持的聚合方式有'Avg'(求平均), 'Count'（计数）, 'Max'（最大）, 'Min'（最小）, 'StdDev'（标准差）,
 'Sum'（求和）, 'Variance'（方差）,见django.db.models.aggregates中的定义

本例中使用的数据库为postgresql， postgresql 在聚合时不支持聚合函数group_concat
我们首先在postgresql中自定义聚合函数如下：
CREATE AGGREGATE group_concat(anyelement)
(
    sfunc = array_append, -- 每行的操作函数，将本行append到数组里
    stype = anyarray,  -- 聚集后返回数组类型
    initcond = '{}'    -- 初始化空数组
);

自定义的聚合函数会自动保存在对应的db中，对于docker启动的pg来说，只需要把对应的db映射出来即可实现自定义函数的
持久化

在pg中增加了group_concat函数后，我们可以继续添加group_concat的聚合方法，见my_concat.py

'''