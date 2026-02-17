"""
Equipment models for ClapLog.
Track cameras, lenses, lighting, and other production equipment.
"""

from django.db import models
from apps.productions.models import Production
from django.conf import settings


class Equipment(models.Model):
    """Production equipment inventory."""

    CATEGORY_CHOICES = [
        ('camera', 'Camera'),
        ('lens', 'Lens'),
        ('lighting', 'Lighting'),
        ('grip', 'Grip'),
        ('electric', 'Electric'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('maintenance', 'Maintenance'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='equipment'
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'equipment'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class EquipmentCheckout(models.Model):
    """Track equipment checkouts."""

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='checkouts')
    checked_out_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipment_checkouts'
    )
    checked_out_at = models.DateTimeField(auto_now_add=True)
    due_back_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    condition_out = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    condition_in = models.CharField(max_length=20, choices=CONDITION_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'equipment_checkout'
        ordering = ['-checked_out_at']

    def __str__(self):
        return f"{self.equipment.name} - {self.checked_out_by.username}"