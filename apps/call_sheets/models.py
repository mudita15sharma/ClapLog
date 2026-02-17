"""
Call Sheet models for ClapLog.
Manages daily shooting schedules.
"""

from django.db import models
from django.conf import settings
from apps.productions.models import Production
from apps.scenes.models import Scene


class CallSheet(models.Model):
    """Daily call sheet for production."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('in_progress', 'In Progress'),
        ('wrapped', 'Wrapped'),
        ('cancelled', 'Cancelled'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='call_sheets'
    )

    shoot_date = models.DateField(db_index=True)
    day_number = models.IntegerField(null=True, blank=True, help_text="Shooting day number")
    call_time = models.TimeField()
    crew_call_time = models.TimeField(null=True, blank=True)
    wrap_time_estimate = models.TimeField(null=True, blank=True)

    location_address = models.TextField(blank=True)
    parking_info = models.TextField(blank=True)

    weather_forecast = models.CharField(max_length=255, blank=True)
    sunrise_time = models.TimeField(null=True, blank=True)
    sunset_time = models.TimeField(null=True, blank=True)

    meals_provided = models.JSONField(default=list, blank=True)
    nearest_hospital = models.TextField(blank=True)
    safety_notes = models.TextField(blank=True)
    general_notes = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_call_sheets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'call_sheets'
        ordering = ['-shoot_date']

    def __str__(self):
        return f"Call Sheet - {self.shoot_date} ({self.production.title})"


class CallSheetScene(models.Model):
    """Scenes scheduled for a call sheet."""

    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='scenes')
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    scheduled_time = models.TimeField(null=True, blank=True)
    estimated_duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    sequence_order = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'call_sheet_scenes'
        unique_together = ['call_sheet', 'scene']
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.scene.scene_number} on {self.call_sheet.shoot_date}"


class CastMember(models.Model):
    """Cast member in a production."""

    ROLE_TYPE_CHOICES = [
        ('lead', 'Lead'),
        ('supporting', 'Supporting'),
        ('day_player', 'Day Player'),
        ('extra', 'Extra'),
        ('stunt', 'Stunt'),
    ]

    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='cast_members')
    name = models.CharField(max_length=255)
    character_name = models.CharField(max_length=255, blank=True)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, default='supporting')

    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cast_members'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} as {self.character_name}" if self.character_name else self.name


class CallSheetCast(models.Model):
    """Cast members scheduled for a call sheet."""

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('on_set', 'On Set'),
        ('wrapped', 'Wrapped'),
        ('cancelled', 'Cancelled'),
    ]

    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='cast')
    cast_member = models.ForeignKey(CastMember, on_delete=models.CASCADE)
    call_time = models.TimeField()
    pickup_location = models.CharField(max_length=255, blank=True)
    makeup_time = models.TimeField(null=True, blank=True)
    scenes_today = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        db_table = 'call_sheet_cast'

    def __str__(self):
        return f"{self.cast_member.name} - {self.call_sheet.shoot_date}"