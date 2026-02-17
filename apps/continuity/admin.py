from django.contrib import admin
from .models import ContinuityNote

@admin.register(ContinuityNote)
class ContinuityNoteAdmin(admin.ModelAdmin):
    list_display = (
        'scene',
        'category',
        'severity',
        'status',
        'actor_character',
        'created_at',
    )
    list_filter = ['category', 'status', 'severity']
    search_fields = ('description', 'warnings', 'actor_character')
    ordering = ('-created_at',)
