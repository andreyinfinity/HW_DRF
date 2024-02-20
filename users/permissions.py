from rest_framework.permissions import BasePermission


class ModeratorPermissionsClass(BasePermission):
    """Проверка является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class OwnerPermissionsClass(BasePermission):
    """Проверка является ли пользователь владельцем"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
