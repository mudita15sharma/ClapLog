"""
Continuity tracking models.
"""
from django.db import models
from apps.scenes.models import Scene


class ContinuityNote(models.Model):
    """Continuity notes for tracking details across scenes."""

    CATEGORY_CHOICES = [
        ('costume', 'Costume'),
        ('props', 'Props'),
        ('makeup', 'Makeup'),
        ('hair', 'Hair'),
        ('lighting', 'Lighting'),
        ('camera', 'Camera'),
        ('script', 'Script'),
        ('other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('flagged', 'Flagged'),
        ('archived', 'Archived'),
    ]

    scene = models.ForeignKey(
        Scene,
        on_delete=models.CASCADE,
        null=True,
        related_name='continuity_notes',
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField()
    actor_character = models.CharField(max_length=200, blank=True)
    warnings = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'continuity_notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} - Scene {self.scene.scene_number}"