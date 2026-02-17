from django.contrib import admin
from .models import ProductionStatistics, DailyProgress


@admin.register(ProductionStatistics)
class ProductionStatisticsAdmin(admin.ModelAdmin):
    list_display = ['production', 'completion_percentage', 'total_scenes', 'completed_scenes', 'last_updated']
    readonly_fields = ['last_updated']


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = ['production', 'date', 'scenes_completed', 'shots_completed', 'pages_shot']
    list_filter = ['date', 'production']
    date_hierarchy = 'date'