#coding : utf-8

from rest_framework import filters, exceptions

class MyFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(age__gt=30)
