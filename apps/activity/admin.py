from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'entity_type', 'description', 'created_at']
    list_filter = ['action_type', 'entity_type', 'created_at']
    search_fields = ['description', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'