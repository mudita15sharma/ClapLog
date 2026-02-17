"""
Admin configuration for Scenes app.
"""

from django.contrib import admin
from .models import Scene


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = [
        'scene_number',
        'scene_name',
        'production',
        'location_text',
        'interior_exterior',
        'day_night',
        'status',
        'shooting_date'
    ]
    list_filter = [
        'status',
        'interior_exterior',
        'day_night',
        'shooting_date',
        'production'
    ]
    search_fields = [
        'scene_number',
        'scene_name',
        'location_text',
        'description'
    ]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Scene Identification', {
            'fields': ('production', 'scene_number', 'scene_name', 'sequence_order')
        }),
        ('Scene Details', {
            'fields': (
                'description',
                'location_text',
                'interior_exterior',
                'day_night',
                'script_day'
            )
        }),
        ('Production Planning', {
            'fields': (
                'script_pages',
                'estimated_duration',
                'actual_duration',
                'priority'
            )
        }),
        ('Scheduling', {
            'fields': (
                'status',
                'shooting_date',
                'call_time',
                'wrap_time'
            )
        }),
        ('Requirements', {
            'fields': (
                'cast_required',
                'crew_required',
                'equipment_needed',
                'special_effects'
            ),
            'classes': ('collapse',)
        }),
        ('Special Requirements', {
            'fields': (
                'stunts_required',
                'vfx_required',
                'weather_dependent'
            ),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    ordering = ['production', 'sequence_order', 'scene_number']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('production')