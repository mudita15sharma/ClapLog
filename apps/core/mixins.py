"""
Reusable model and view mixins for ClapLog.
"""

from django.db import models


class UserTrackingMixin(models.Model):
    """
    Mixin to track which user created/updated an object.
    """
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True


class OrderingMixin(models.Model):
    """
    Mixin for models that need custom ordering.
    """
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order']


class StatusMixin(models.Model):
    """
    Mixin for models with status tracking.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )

    class Meta:
        abstract = True

    def is_active(self):
        return self.status == 'active'

    def is_completed(self):
        return self.status == 'completed'