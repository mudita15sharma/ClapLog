"""
Props models for ClapLog.
Manage props and set dressing items.
"""

from django.db import models
from django.conf import settings
from apps.productions.models import Production
from apps.scenes.models import Scene


class Prop(models.Model):
    """Props and set dressing items."""

    CATEGORY_CHOICES = [
        ('hand_prop', 'Hand Prop'),
        ('set_dressing', 'Set Dressing'),
        ('vehicle', 'Vehicle'),
        ('weapon', 'Weapon'),
        ('food', 'Food/Beverage'),
        ('document', 'Document/Paper'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('costume_prop', 'Costume Prop'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('needed', 'Needed'),
        ('sourced', 'Sourced'),
        ('purchased', 'Purchased'),
        ('rented', 'Rented'),
        ('ready', 'Ready'),
        ('on_set', 'On Set'),
        ('returned', 'Returned'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='props'
    )
    scene = models.ForeignKey(
        Scene,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='props',
        help_text="Scene where this prop is used"
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='needed', db_index=True)

    source = models.CharField(max_length=255, blank=True, help_text="Where to get this prop")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_rented = models.BooleanField(default=False)
    rental_return_date = models.DateField(null=True, blank=True)


    brand_model = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=100, blank=True)
    size_dimensions = models.CharField(max_length=100, blank=True)

    continuity_notes = models.TextField(blank=True)
    hero_prop = models.BooleanField(default=False, help_text="Is this a hero/featured prop?")

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_props'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'props'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"