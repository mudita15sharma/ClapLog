"""
Continuity Notes serializers.
"""
from rest_framework import serializers
from .models import ContinuityNote


class ContinuityNoteSerializer(serializers.ModelSerializer):
    """Serializer for continuity notes."""

    scene_number = serializers.CharField(source='scene.scene_number', read_only=True)

    class Meta:
        model = ContinuityNote
        fields = [
            'id',
            'scene',
            'scene_number',
            'category',
            'severity',
            'status',
            'description',
            'actor_character',
            'warnings',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'scene_number']

    def validate_description(self, value):
        """Ensure description is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value