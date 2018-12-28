from django.contrib import admin
from . import models

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'favorates', 'school')
    search_fields = ('name', 'age', 'favorates', 'school__name')
    list_filter = ('school__name',)

    # 可以根据需求限制get请求的qset
    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        # 可以根据需求限制get请求的qset
        # TODO
        return qs

    def save_model(self, request, obj, form, change):
        # 可以根据需求在保存前增加操作
        # TODO
        super(PersonAdmin, self).save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonAdmin, self).get_search_results(request, queryset, search_term)
        # 可以根据需求增加搜索条件
        # TODO
        return queryset, use_distinct

    def delete_model(self, request, obj):
        # 可以根据需求增加删除前的操作
        # TODO
        super(PersonAdmin, self).delete_model(request, obj)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

# Register your models here.
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Book)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.PersonBookRelation)
