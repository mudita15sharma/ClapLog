from django.contrib import admin
from .models import ExportJob


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = ['export_type', 'user', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'export_type', 'created_at']
    readonly_fields = ['created_at', 'started_at', 'completed_at']