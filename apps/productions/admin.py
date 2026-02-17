"""
Admin configuration for Productions app.
"""

from django.contrib import admin
from .models import Production, ProductionTeam


class ProductionTeamInline(admin.TabularInline):
    """Inline for production team members."""
    model = ProductionTeam
    extra = 1
    fields = ['user', 'role', 'permissions']


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'director',
        'status',
        'start_date',
        'end_date',
        'created_by',
        'created_at'
    ]
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['title', 'director', 'production_company']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'director', 'production_company', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Budget & Details', {
            'fields': ('budget', 'genre', 'runtime_minutes', 'aspect_ratio', 'description')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [ProductionTeamInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductionTeam)
class ProductionTeamAdmin(admin.ModelAdmin):
    list_display = ['production', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['production__title', 'user__username', 'role']