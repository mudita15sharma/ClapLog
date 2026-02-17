from django.contrib import admin
from .models import CallSheet, CallSheetScene, CastMember, CallSheetCast


@admin.register(CallSheet)
class CallSheetAdmin(admin.ModelAdmin):
    list_display = ['shoot_date', 'production', 'status', 'call_time']
    list_filter = ['status', 'shoot_date']


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'character_name', 'role_type', 'production']
    list_filter = ['role_type']
    search_fields = ['name', 'character_name']


admin.site.register(CallSheetScene)
admin.site.register(CallSheetCast)