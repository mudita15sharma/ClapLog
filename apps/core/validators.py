"""
Custom validators for ClapLog models.
"""

from django.core.exceptions import ValidationError
import re


def validate_scene_number(value):
    """
    Validate scene number format.
    Examples: 1, 2A, 15B, 100
    """
    pattern = r'^\d+[A-Z]?$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Scene number must be a number optionally followed by a letter (e.g., 1, 2A, 15B)'
        )


def validate_shot_number(value):
    """
    Validate shot number format.
    Examples: 1, 2A, 15B, 100-1
    """
    pattern = r'^\d+(-\d+)?[A-Z]?$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Shot number must be a number, optionally with hyphen and number, optionally followed by a letter'
        )


def validate_phone_number(value):
    """
    Simple phone number validation.
    """
    cleaned = re.sub(r'[\s\-\(\)\+]', '', value)

    if not cleaned.isdigit() or len(cleaned) < 10:
        raise ValidationError(
            'Enter a valid phone number with at least 10 digits'
        )


def validate_timecode(value):
    """
    Validate timecode format (HH:MM:SS or HH:MM:SS:FF).
    """
    pattern = r'^\d{2}:\d{2}:\d{2}(:\d{2})?$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Timecode must be in format HH:MM:SS or HH:MM:SS:FF'
        )