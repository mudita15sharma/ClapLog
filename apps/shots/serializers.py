"""
Shot serializers for ClapLog API.
"""

from rest_framework import serializers
from .models import Shot, Take


class TakeSerializer(serializers.ModelSerializer):
    """Take serializer."""

    class Meta:
        model = Take
        fields = [
            'id',
            'shot',
            'take_number',
            'duration',
            'is_selected',
            'quality_rating',
            'notes',
            'issues',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ShotSerializer(serializers.ModelSerializer):
    """Main shot serializer."""

    takes = TakeSerializer(many=True, read_only=True)

    class Meta:
        model = Shot
        fields = [
            'id',
            'scene',
            'shot_number',
            'shot_name',
            'description',
            'shot_type',
            'camera_angle',
            'camera_movement',
            'camera_model',
            'lens',
            'focal_length',
            'aperture',
            'iso',
            'frame_rate',
            'duration',
            'takes_planned',
            'takes_completed',
            'best_take',
            'status',
            'vfx_required',
            'vfx_notes',
            'sound_notes',
            'lighting_setup',
            'notes',
            'sequence_order',
            'created_at',
            'updated_at',
            'takes',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShotListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing shots."""

    class Meta:
        model = Shot
        fields = [
            'id',
            'shot_number',
            'shot_name',
            'shot_type',
            'status',
            'takes_completed',
        ]