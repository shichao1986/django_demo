#coding : utf-8

# 私有permissions

from rest_framework import permissions

class MyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        if obj.age > 30:
            return True
        return False