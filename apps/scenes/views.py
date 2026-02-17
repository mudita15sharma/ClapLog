"""
Scene API views.
"""
from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Scene
from .serializers import SceneSerializer, SceneListSerializer


class SceneViewSet(viewsets.ModelViewSet):
    """API endpoint for scenes."""

    queryset = Scene.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['production', 'status', 'interior_exterior', 'day_night', 'shooting_date']
    search_fields = ['scene_number', 'scene_name', 'location_text', 'description']
    ordering_fields = ['scene_number', 'shooting_date', 'created_at', 'sequence_order']

    def get_serializer_class(self):
        if self.action == 'list':
            return SceneListSerializer
        return SceneSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        production_id = self.request.query_params.get('production_id')

        if production_id:
            queryset = queryset.filter(production_id=production_id)

        user = self.request.user
        queryset = queryset.filter(
            models.Q(production__created_by=user) |
            models.Q(production__team_members__user=user)
        ).distinct()

        return queryset

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update scene status."""
        scene = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Scene.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        scene.status = new_status
        scene.save()

        serializer = self.get_serializer(scene)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create scenes."""
        scenes_data = request.data.get('scenes', [])

        if not scenes_data:
            return Response(
                {'error': 'No scenes provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=scenes_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def shots(self, request, pk=None):
        """Get all shots for this scene."""
        scene = self.get_object()
        from apps.shots.serializers import ShotListSerializer

        shots = scene.shots.all()
        serializer = ShotListSerializer(shots, many=True)
        return Response(serializer.data)