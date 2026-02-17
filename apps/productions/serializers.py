"""
Productions serializer with live scene/shot counts.
"""
from rest_framework import serializers
from .models import Production


class ProductionSerializer(serializers.ModelSerializer):
    """Serializer with live computed stats."""

    scene_count             = serializers.SerializerMethodField()
    shot_count              = serializers.SerializerMethodField()
    completed_scene_count   = serializers.SerializerMethodField()
    in_progress_scene_count = serializers.SerializerMethodField()
    completion_percentage   = serializers.SerializerMethodField()

    class Meta:
        model  = Production
        fields = '__all__'

    def _get_scenes(self, obj):
        """
        Safely get scenes queryset.
        Tries 'scenes' related name first, then 'scene_set' fallback.
        """
        if hasattr(obj, 'scenes'):
            return obj.scenes.all()
        elif hasattr(obj, 'scene_set'):
            return obj.scene_set.all()
        return []

    def get_scene_count(self, obj):
        try:
            scenes = self._get_scenes(obj)
            return scenes.count() if hasattr(scenes, 'count') else len(scenes)
        except Exception:
            return 0

    def get_shot_count(self, obj):
        try:
            scenes = self._get_scenes(obj)
            total = 0
            for scene in scenes:
                if hasattr(scene, 'shots'):
                    total += scene.shots.count()
                elif hasattr(scene, 'shot_set'):
                    total += scene.shot_set.count()
            return total
        except Exception:
            return 0

    def get_completed_scene_count(self, obj):
        try:
            scenes = self._get_scenes(obj)
            if hasattr(scenes, 'filter'):
                return scenes.filter(status='completed').count()
            return sum(1 for s in scenes if s.status == 'completed')
        except Exception:
            return 0

    def get_in_progress_scene_count(self, obj):
        try:
            scenes = self._get_scenes(obj)
            if hasattr(scenes, 'filter'):
                return scenes.filter(status='in_progress').count()
            return sum(1 for s in scenes if s.status == 'in_progress')
        except Exception:
            return 0

    def get_completion_percentage(self, obj):
        try:
            total = self.get_scene_count(obj)
            if total == 0:
                return 0
            done = self.get_completed_scene_count(obj)
            return round((done / total) * 100, 1)
        except Exception:
            return 0