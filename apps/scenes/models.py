"""
Scene models for ClapLog.
Manages individual scenes within a production.
"""

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.productions.models import Production


class Scene(models.Model):
    """
    Scene model representing a scene from the script.
    """

    INT_EXT_CHOICES = [
        ('INT', 'Interior'),
        ('EXT', 'Exterior'),
        ('INT/EXT', 'Interior/Exterior'),
    ]

    DAY_NIGHT_CHOICES = [
        ('DAY', 'Day'),
        ('NIGHT', 'Night'),
        ('DAWN', 'Dawn'),
        ('DUSK', 'Dusk'),
        ('CONTINUOUS', 'Continuous'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='scenes',
        help_text="Production this scene belongs to"
    )

    scene_number = models.CharField(
        max_length=20,
        db_index=True,
        help_text="Scene number from script (e.g., '1', '2A', '15')"
    )
    scene_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional scene name or slug line"
    )

    description = models.TextField(
        blank=True,
        help_text="Scene description or action"
    )
    location_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Location description (e.g., 'COFFEE SHOP', 'PARK')"
    )
    interior_exterior = models.CharField(
        max_length=10,
        choices=INT_EXT_CHOICES,
        default='INT',
        help_text="Interior or Exterior"
    )
    day_night = models.CharField(
        max_length=15,
        choices=DAY_NIGHT_CHOICES,
        default='DAY',
        help_text="Time of day"
    )

    script_pages = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.1'))],
        help_text="Number of script pages (e.g., 2.5)"
    )
    estimated_duration = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Estimated duration in minutes"
    )
    actual_duration = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Actual duration filmed in minutes"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started',
        db_index=True,
        help_text="Current scene status"
    )
    shooting_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Scheduled shooting date"
    )
    call_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Call time for this scene"
    )
    wrap_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Actual wrap time"
    )

    cast_required = models.JSONField(
        default=list,
        blank=True,
        help_text="List of cast members required (JSON array)"
    )
    crew_required = models.JSONField(
        default=list,
        blank=True,
        help_text="List of crew positions required (JSON array)"
    )
    equipment_needed = models.TextField(
        blank=True,
        help_text="Equipment needed for this scene"
    )

    special_effects = models.TextField(
        blank=True,
        help_text="Special effects notes"
    )
    stunts_required = models.BooleanField(
        default=False,
        help_text="Indicates if stunts are required"
    )
    vfx_required = models.BooleanField(
        default=False,
        help_text="Indicates if VFX is required"
    )
    weather_dependent = models.BooleanField(
        default=False,
        help_text="Indicates if scene is weather dependent"
    )

    notes = models.TextField(
        blank=True,
        help_text="General notes about the scene"
    )
    priority = models.IntegerField(
        default=0,
        help_text="Priority level (higher = more important)"
    )
    sequence_order = models.IntegerField(
        default=0,
        db_index=True,
        help_text="Order in which scene appears in script"
    )
    script_day = models.CharField(
        max_length=50,
        blank=True,
        help_text="Script day (e.g., 'Day 1', 'Night 2')"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'scenes'
        unique_together = ['production', 'scene_number']
        ordering = ['sequence_order', 'scene_number']
        verbose_name = 'scene'
        verbose_name_plural = 'scenes'
        indexes = [
            models.Index(fields=['production']),
            models.Index(fields=['status']),
            models.Index(fields=['shooting_date']),
            models.Index(fields=['sequence_order']),
            models.Index(fields=['production', 'status']),
        ]

    def __str__(self):
        location = self.scene_name or self.location_text
        return f"Scene {self.scene_number}" + (f" - {location}" if location else "")

    @property
    def slug_line(self):
        """Generate traditional slug line format."""
        parts = []
        if self.interior_exterior:
            parts.append(self.interior_exterior)
        if self.location_text:
            parts.append(self.location_text.upper())
        if self.day_night:
            parts.append(self.day_night)
        return ". ".join(parts) if parts else ""

    @property
    def total_shots(self):
        """Get total number of shots in this scene."""
        return self.shots.count()

    @property
    def completed_shots(self):
        """Get number of completed shots."""
        return self.shots.filter(status='completed').count()

    @property
    def shot_completion_percentage(self):
        """Calculate shot completion percentage for this scene."""
        total = self.total_shots
        if total == 0:
            return 0
        completed = self.completed_shots
        return round((completed / total) * 100, 2)

    @property
    def is_completed(self):
        """Check if scene is completed."""
        return self.status == 'completed'

    @property
    def is_scheduled(self):
        """Check if scene has a shooting date."""
        return self.shooting_date is not None

    def mark_completed(self):
        """Mark scene as completed."""
        self.status = 'completed'
        self.save(update_fields=['status', 'updated_at'])

    def mark_in_progress(self):
        """Mark scene as in progress."""
        self.status = 'in_progress'
        self.save(update_fields=['status', 'updated_at'])