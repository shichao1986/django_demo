#coding : utf-8

# 私有permissions

from rest_framework import permissions

class MyPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False