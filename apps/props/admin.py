from django.contrib import admin
from .models import Prop


@admin.register(Prop)
class PropAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'status', 'production', 'scene']
    list_filter = ['category', 'status', 'hero_prop', 'is_rented']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'