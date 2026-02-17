"""
Utility functions for ClapLog.
"""

import os
from datetime import datetime, timedelta
from django.utils import timezone


def generate_unique_filename(instance, filename):
    """
    Generate a unique filename for uploaded files.
    """
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{instance.__class__.__name__.lower()}_{timestamp}.{ext}"


def get_client_ip(request):
    """
    Get the client's IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_shooting_days(start_date, end_date):
    """
    Calculate the number of shooting days between two dates.
    Excludes weekends.
    """
    if not start_date or not end_date:
        return 0

    days = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:
            days += 1
        current_date += timedelta(days=1)

    return days


def format_duration(seconds):
    """
    Format duration in seconds to human-readable format.
    """
    if not seconds:
        return "0s"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def get_file_size_display(bytes_size):
    """
    Convert bytes to human-readable file size.
    """
    if not bytes_size:
        return "0 B"

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0

    return f"{bytes_size:.1f} PB"


def log_activity(user, action_type, entity_type, entity_id, description, production=None, metadata=None):
    """
    Helper function to log user activities.
    """
    from apps.activity.models import ActivityLog

    ActivityLog.objects.create(
        user=user,
        production=production,
        action_type=action_type,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
        metadata=metadata or {}
    )