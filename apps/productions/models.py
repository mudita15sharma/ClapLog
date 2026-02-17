"""
Production models for ClapLog.
Manages film production projects and team members.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Production(models.Model):
    """
    Main production/project model.
    Represents a film, TV show, commercial, or any video production project.
    """

    STATUS_CHOICES = [
        ('pre_production', 'Pre-Production'),
        ('production', 'Production'),
        ('post_production', 'Post-Production'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Production title"
    )
    director = models.CharField(
        max_length=255,
        blank=True,
        help_text="Director name"
    )
    production_company = models.CharField(
        max_length=255,
        blank=True,
        help_text="Production company name"
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Production start date"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Production end date"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pre_production',
        db_index=True,
        help_text="Current production status"
    )

    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total production budget"
    )
    description = models.TextField(
        blank=True,
        help_text="Production description/synopsis"
    )
    genre = models.CharField(
        max_length=100,
        blank=True,
        help_text="Genre (Drama, Action, Comedy, etc.)"
    )
    runtime_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Expected runtime in minutes"
    )
    aspect_ratio = models.CharField(
        max_length=20,
        blank=True,
        help_text="Aspect ratio (16:9, 2.35:1, etc.)"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_productions',
        help_text="User who created this production"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productions'
        ordering = ['-created_at']
        verbose_name = 'production'
        verbose_name_plural = 'productions'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
            models.Index(fields=['created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def total_scenes(self):
        """Get total number of scenes."""
        return self.scenes.count()

    @property
    def completed_scenes(self):
        """Get number of completed scenes."""
        return self.scenes.filter(status='completed').count()

    @property
    def total_shots(self):
        """Get total number of shots across all scenes."""
        return sum(scene.shots.count() for scene in self.scenes.all())

    @property
    def completion_percentage(self):
        """Calculate production completion percentage."""
        total = self.total_scenes
        if total == 0:
            return 0
        completed = self.completed_scenes
        return round((completed / total) * 100, 2)

    @property
    def total_script_pages(self):
        """Calculate total script pages."""
        return sum(scene.script_pages or 0 for scene in self.scenes.all())

    @property
    def days_until_start(self):
        """Calculate days until production starts."""
        if not self.start_date:
            return None
        from datetime import date
        delta = self.start_date - date.today()
        return delta.days

    @property
    def is_active(self):
        """Check if production is currently active."""
        return self.status in ['pre_production', 'production']


class ProductionTeam(models.Model):
    """
    Junction model for production team members.
    Links users to productions with specific roles and permissions.
    """

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='team_members',
        help_text="Production this team member belongs to"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='production_roles',
        help_text="User who is part of this production"
    )
    role = models.CharField(
        max_length=100,
        help_text="Role in this specific production"
    )
    permissions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom permissions for this team member"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'production_teams'
        unique_together = ['production', 'user']
        verbose_name = 'production team member'
        verbose_name_plural = 'production team members'
        indexes = [
            models.Index(fields=['production']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role} on {self.production.title}"

    def has_permission(self, permission_type):
        """
        Check if team member has specific permission.

        Args:
            permission_type: String like 'can_edit_scenes', 'can_delete_shots'

        Returns:
            bool: True if has permission
        """
        return self.permissions.get(permission_type, False)

    def grant_permission(self, permission_type):
        """Grant a specific permission to team member."""
        self.permissions[permission_type] = True
        self.save()

    def revoke_permission(self, permission_type):
        """Revoke a specific permission from team member."""
        self.permissions[permission_type] = False
        self.save()