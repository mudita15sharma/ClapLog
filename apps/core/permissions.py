"""
Custom permissions for ClapLog.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user


class IsProductionMember(permissions.BasePermission):
    """
    Permission to check if user is a member of the production.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'production'):
            production = obj.production
        elif hasattr(obj, 'scene'):
            production = obj.scene.production
        else:
            return False

        if production.created_by == request.user:
            return True

        return production.team_members.filter(user=request.user).exists()


class IsDirectorOrProducer(permissions.BasePermission):
    """
    Permission for directors and producers only.
    """

    def has_permission(self, request, view):
        return request.user.role in ['director', 'producer', 'admin']


class IsAdminUser(permissions.BasePermission):
    """
    Permission for admin users only.
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.role == 'admin'


class CanManageProduction(permissions.BasePermission):
    """
    Check if user can manage a production (create, update, delete).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True

        if request.user.role in ['director', 'producer', 'admin']:
            return True

        return False