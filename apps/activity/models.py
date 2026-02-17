"""
Activity Log models for ClapLog.
Track all user actions and changes in productions.
"""

from django.db import models
from django.conf import settings
from apps.productions.models import Production


class ActivityLog(models.Model):
    """Log of all user activities in the system."""

    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
        ('export', 'Exported'),
        ('publish', 'Published'),
        ('archive', 'Archived'),
    ]

    ENTITY_CHOICES = [
        ('production', 'Production'),
        ('scene', 'Scene'),
        ('shot', 'Shot'),
        ('call_sheet', 'Call Sheet'),
        ('continuity', 'Continuity Note'),
        ('cast_member', 'Cast Member'),
        ('equipment', 'Equipment'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    entity_type = models.CharField(max_length=50, choices=ENTITY_CHOICES, db_index=True)
    entity_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'activity_log'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'action_type']),
            models.Index(fields=['entity_type', 'entity_id']),
        ]

    def __str__(self):
        return f"{self.user.username} {self.action_type} {self.entity_type} at {self.created_at}"