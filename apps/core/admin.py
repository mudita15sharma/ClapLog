"""
Core admin configurations and mixins.
"""

from django.contrib import admin


class ReadOnlyAdminMixin:
    """
    Mixin to make admin read-only.
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TimestampAdminMixin:
    """
    Mixin to add timestamp fields to readonly.
    """
    readonly_fields = ['created_at', 'updated_at']


class UserTrackingAdminMixin:
    """
    Mixin to track user actions in admin.
    """
    readonly_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)