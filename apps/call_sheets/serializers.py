"""
Call Sheet serializers for ClapLog API.
"""

from rest_framework import serializers
from .models import CallSheet, CallSheetScene, CastMember, CallSheetCast
from apps.users.serializers import UserListSerializer


class CastMemberSerializer(serializers.ModelSerializer):
    """Cast member serializer."""

    class Meta:
        model = CastMember
        fields = [
            'id',
            'production',
            'name',
            'character_name',
            'role_type',
            'contact_phone',
            'contact_email',
            'notes',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

class CastMemberDetailSerializer(serializers.ModelSerializer):
    """Detailed cast member serializer with additional info."""

    total_scenes = serializers.SerializerMethodField()
    total_call_sheets = serializers.SerializerMethodField()

    class Meta:
        model = CastMember
        fields = [
            'id',
            'production',
            'name',
            'character_name',
            'role_type',
            'contact_phone',
            'contact_email',
            'notes',
            'created_at',
            'updated_at',
            'total_scenes',
            'total_call_sheets',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_scenes(self, obj):
        return obj.callsheetcast_set.count()

    def get_total_call_sheets(self, obj):
        return obj.callsheetcast_set.values('call_sheet').distinct().count()



class CallSheetSceneSerializer(serializers.ModelSerializer):
    """Call sheet scene serializer."""

    scene_id = serializers.IntegerField(write_only=True)
    scene_number = serializers.CharField(source='scene.scene_number', read_only=True)
    scene_name = serializers.CharField(source='scene.scene_name', read_only=True)

    class Meta:
        model = CallSheetScene
        fields = [
            'id',
            'call_sheet',
            'scene_id',
            'scene_number',
            'scene_name',
            'scheduled_time',
            'estimated_duration',
            'sequence_order',
            'notes',
        ]
        read_only_fields = ['id']


class CallSheetCastSerializer(serializers.ModelSerializer):
    """Call sheet cast serializer."""

    cast_member_id = serializers.IntegerField(write_only=True)
    cast_name = serializers.CharField(source='cast_member.name', read_only=True)
    character_name = serializers.CharField(source='cast_member.character_name', read_only=True)

    class Meta:
        model = CallSheetCast
        fields = [
            'id',
            'call_sheet',
            'cast_member_id',
            'cast_name',
            'character_name',
            'call_time',
            'pickup_location',
            'makeup_time',
            'scenes_today',
            'notes',
            'status',
        ]
        read_only_fields = ['id']


class CallSheetSerializer(serializers.ModelSerializer):
    """Main call sheet serializer."""

    scenes = CallSheetSceneSerializer(many=True, read_only=True)
    cast = CallSheetCastSerializer(many=True, read_only=True)
    created_by = UserListSerializer(read_only=True)

    class Meta:
        model = CallSheet
        fields = [
            'id',
            'production',
            'shoot_date',
            'day_number',
            'call_time',
            'crew_call_time',
            'wrap_time_estimate',
            'location_address',
            'parking_info',
            'weather_forecast',
            'sunrise_time',
            'sunset_time',
            'meals_provided',
            'nearest_hospital',
            'safety_notes',
            'general_notes',
            'status',
            'published_at',
            'created_by',
            'created_at',
            'updated_at',
            'scenes',
            'cast',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class CallSheetListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing call sheets."""

    scene_count = serializers.SerializerMethodField()

    class Meta:
        model = CallSheet
        fields = [
            'id',
            'shoot_date',
            'call_time',
            'status',
            'scene_count',
        ]

    def get_scene_count(self, obj):
        return obj.scenes.count()