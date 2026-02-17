"""
Props serializers for ClapLog API.
"""

from rest_framework import serializers
from .models import Prop


class PropSerializer(serializers.ModelSerializer):
    """Full prop serializer."""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    scene_number = serializers.CharField(source='scene.scene_number', read_only=True)

    class Meta:
        model = Prop
        fields = [
            'id',
            'production',
            'scene',
            'scene_number',
            'name',
            'category',
            'category_display',
            'description',
            'quantity',
            'status',
            'status_display',
            'source',
            'cost',
            'is_rented',
            'rental_return_date',
            'brand_model',
            'color',
            'size_dimensions',
            'continuity_notes',
            'hero_prop',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PropListSerializer(serializers.ModelSerializer):
    """Lightweight prop list serializer."""

    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Prop
        fields = [
            'id',
            'name',
            'category',
            'category_display',
            'quantity',
            'status',
            'status_display',
            'hero_prop',
            'cost',
        ]