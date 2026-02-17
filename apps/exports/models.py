"""
Export models for ClapLog.
Track export jobs and generated files.
"""

from django.db import models
from django.conf import settings
from apps.productions.models import Production


class ExportJob(models.Model):
    """Track data export jobs."""

    EXPORT_TYPE_CHOICES = [
        ('scenes_csv', 'Scenes CSV'),
        ('shots_csv', 'Shots CSV'),
        ('call_sheets_csv', 'Call Sheets CSV'),
        ('continuity_csv', 'Continuity CSV'),
        ('production_book_excel', 'Production Book Excel'),
        ('call_sheet_pdf', 'Call Sheet PDF'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    production = models.ForeignKey(
        Production,
        on_delete=models.CASCADE,
        related_name='export_jobs'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='export_jobs'
    )
    export_type = models.CharField(max_length=30, choices=EXPORT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="Size in bytes")
    error_message = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'export_jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_export_type_display()} - {self.status}"