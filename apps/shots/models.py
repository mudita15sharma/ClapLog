"""
Shot models for ClapLog.
Manages individual camera shots within scenes.
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.scenes.models import Scene


class Shot(models.Model):
    """Individual camera shot within a scene."""

    SHOT_TYPE_CHOICES = [
        ('WIDE', 'Wide Shot'),
        ('MEDIUM', 'Medium Shot'),
        ('CLOSE_UP', 'Close-Up'),
        ('EXTREME_CLOSE_UP', 'Extreme Close-Up'),
        ('TWO_SHOT', 'Two Shot'),
        ('OVER_SHOULDER', 'Over Shoulder'),
        ('POV', 'Point of View'),
        ('INSERT', 'Insert'),
        ('ESTABLISHING', 'Establishing Shot'),
        ('MASTER', 'Master Shot'),
    ]

    CAMERA_ANGLE_CHOICES = [
        ('EYE_LEVEL', 'Eye Level'),
        ('HIGH_ANGLE', 'High Angle'),
        ('LOW_ANGLE', 'Low Angle'),
        ('DUTCH_ANGLE', 'Dutch Angle'),
        ('AERIAL', 'Aerial'),
        ('BIRDS_EYE', 'Birds Eye'),
    ]

    CAMERA_MOVEMENT_CHOICES = [
        ('STATIC', 'Static'),
        ('PAN', 'Pan'),
        ('TILT', 'Tilt'),
        ('DOLLY', 'Dolly'),
        ('TRACKING', 'Tracking'),
        ('CRANE', 'Crane'),
        ('HANDHELD', 'Handheld'),
        ('STEADICAM', 'Steadicam'),
        ('ZOOM', 'Zoom'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    ]

    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        related_name='shots',
        help_text="Scene this shot belongs to"
    )

    shot_number = models.CharField(max_length=20, db_index=True)
    shot_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    shot_type = models.CharField(max_length=20, choices=SHOT_TYPE_CHOICES, default='MEDIUM')
    camera_angle = models.CharField(max_length=20, choices=CAMERA_ANGLE_CHOICES, default='EYE_LEVEL')
    camera_movement = models.CharField(max_length=20, choices=CAMERA_MOVEMENT_CHOICES, default='STATIC')

    camera_model = models.CharField(max_length=100, blank=True)
    lens = models.CharField(max_length=50, blank=True, help_text="e.g., 50mm, 24-70mm")
    focal_length = models.CharField(max_length=20, blank=True)
    aperture = models.CharField(max_length=10, blank=True, help_text="e.g., f/2.8")
    iso = models.CharField(max_length=10, blank=True)
    frame_rate = models.IntegerField(default=24, help_text="Frames per second")

    duration = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Duration in seconds"
    )
    takes_planned = models.IntegerField(default=1)
    takes_completed = models.IntegerField(default=0)
    best_take = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', db_index=True)

    vfx_required = models.BooleanField(default=False)
    vfx_notes = models.TextField(blank=True)
    sound_notes = models.TextField(blank=True)
    lighting_setup = models.TextField(blank=True)

    notes = models.TextField(blank=True)
    sequence_order = models.IntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shots'
        unique_together = ['scene', 'shot_number']
        ordering = ['sequence_order', 'shot_number']

    def __str__(self):
        return f"Shot {self.shot_number} - {self.scene}"

    @property
    def is_completed(self):
        return self.status == 'completed'


class Take(models.Model):
    """Individual take of a shot."""

    QUALITY_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    shot = models.ForeignKey(Shot, on_delete=models.CASCADE, related_name='takes')
    take_number = models.IntegerField()
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds")
    is_selected = models.BooleanField(default=False)
    quality_rating = models.IntegerField(choices=QUALITY_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    issues = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'takes'
        unique_together = ['shot', 'take_number']
        ordering = ['take_number']

    def __str__(self):
        return f"Take {self.take_number} - {self.shot}"