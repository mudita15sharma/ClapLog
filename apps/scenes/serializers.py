"""
Scene serializers for ClapLog API.
"""

from rest_framework import serializers
from .models import Scene


class SceneSerializer(serializers.ModelSerializer):
    """Main scene serializer."""

    shot_count = serializers.SerializerMethodField()
    slug_line = serializers.ReadOnlyField()

    class Meta:
        model = Scene
        fields = [
            'id',
            'production',
            'scene_number',
            'scene_name',
            'description',
            'location_text',
            'interior_exterior',
            'day_night',
            'script_pages',
            'estimated_duration',
            'actual_duration',
            'status',
            'shooting_date',
            'call_time',
            'wrap_time',
            'cast_required',
            'crew_required',
            'equipment_needed',
            'special_effects',
            'stunts_required',
            'vfx_required',
            'weather_dependent',
            'notes',
            'priority',
            'sequence_order',
            'script_day',
            'created_at',
            'updated_at',
            'shot_count',
            'slug_line',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_shot_count(self, obj):
        return obj.shots.count()


class SceneListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing scenes."""

    class Meta:
        model = Scene
        fields = [
            'id',
            'scene_number',
            'scene_name',
            'location_text',
            'status',
            'shooting_date',
            'interior_exterior',
            'day_night',
        ]