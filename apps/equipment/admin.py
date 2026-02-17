from django.contrib import admin
from .models import Equipment, EquipmentCheckout


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'status', 'production']
    list_filter = ['category', 'status']
    search_fields = ['name', 'manufacturer', 'model']


@admin.register(EquipmentCheckout)
class EquipmentCheckoutAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'checked_out_by', 'checked_out_at', 'returned_at']
    list_filter = ['checked_out_at', 'returned_at']