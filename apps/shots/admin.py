from django.contrib import admin
from .models import Shot, Take

@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ['shot_number', 'scene', 'shot_type', 'status', 'takes_completed']
    list_filter = ['status', 'shot_type']
    search_fields = ['shot_number', 'description']

@admin.register(Take)
class TakeAdmin(admin.ModelAdmin):
    list_display = ['take_number', 'shot', 'is_selected', 'quality_rating']
    list_filter = ['is_selected', 'quality_rating']