#coding : utf-8

# 私有permissions

from rest_framework import permissions

class MyPermissions(permissions.BasePermission):
    # has_permission 用于检查用户是否有权限访问该view
    def has_permission(self, request, view):
        return True
    # 当has_permission 通过检查后
    # has_object_permission 检查具体数据库中某一条记录是否可以被修改
    # 由于指定了具体的一条记录，所以该检查对应的是put，delete等提供pk的接口
    def has_object_permission(self, request, view, obj):
        if obj.age > 30:
            return True
        return False