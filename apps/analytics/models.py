"""
Analytics models for ClapLog.
Store cached production statistics and metrics.
"""

from django.db import models
from apps.productions.models import Production


class ProductionStatistics(models.Model):
    """Cached production statistics for faster dashboard loading."""

    production = models.OneToOneField(
        Production,
        on_delete=models.CASCADE,
        related_name='statistics'
    )

    total_scenes = models.IntegerField(default=0)
    completed_scenes = models.IntegerField(default=0)
    in_progress_scenes = models.IntegerField(default=0)
    not_started_scenes = models.IntegerField(default=0)

    total_shots = models.IntegerField(default=0)
    completed_shots = models.IntegerField(default=0)

    total_script_pages = models.DecimalField(max_digits=6, decimal_places=1, default=0)

    shooting_days = models.IntegerField(default=0)
    days_completed = models.IntegerField(default=0)

    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    team_size = models.IntegerField(default=0)
    cast_count = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'production_statistics'
        verbose_name_plural = 'Production Statistics'

    def __str__(self):
        return f"Stats for {self.production.title}"


class DailyProgress(models.Model):
    """Track daily production progress."""

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='daily_progress'
    )
    date = models.DateField(db_index=True)
    scenes_completed = models.IntegerField(default=0)
    shots_completed = models.IntegerField(default=0)
    pages_shot = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_progress'
        unique_together = ['production', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.production.title} - {self.date}"