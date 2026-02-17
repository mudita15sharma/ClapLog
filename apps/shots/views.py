"""
Shot API views.
"""
from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shot, Take
from .serializers import ShotSerializer, ShotListSerializer, TakeSerializer


class ShotViewSet(viewsets.ModelViewSet):
    """API endpoint for shots."""

    queryset = Shot.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scene', 'status', 'shot_type', 'camera_angle']
    search_fields = ['shot_number', 'shot_name', 'description']
    ordering_fields = ['shot_number', 'created_at', 'sequence_order']

    def get_serializer_class(self):
        if self.action == 'list':
            return ShotListSerializer
        return ShotSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        scene_id = self.request.query_params.get('scene_id')

        if scene_id:
            queryset = queryset.filter(scene_id=scene_id)

        user = self.request.user
        queryset = queryset.filter(
            models.Q(scene__production__created_by=user) |
            models.Q(scene__production__team_members__user=user)
        ).distinct()

        return queryset

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update shot status."""
        shot = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Shot.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shot.status = new_status
        shot.save()

        serializer = self.get_serializer(shot)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_take(self, request, pk=None):
        """Add a take to this shot."""
        shot = self.get_object()
        data = request.data.copy()
        data['shot'] = shot.id

        serializer = TakeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            shot.takes_completed = shot.takes.count()
            shot.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def select_take(self, request, pk=None):
        """Select best take for this shot."""
        shot = self.get_object()
        take_number = request.data.get('take_number')

        if not take_number:
            return Response(
                {'error': 'take_number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shot.takes.update(is_selected=False)

        try:
            take = shot.takes.get(take_number=take_number)
            take.is_selected = True
            take.save()
            shot.best_take = take_number
            shot.save()

            return Response({'message': f'Take {take_number} selected as best take'})
        except Take.DoesNotExist:
            return Response(
                {'error': 'Take not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class TakeViewSet(viewsets.ModelViewSet):
    """API endpoint for takes."""

    queryset = Take.objects.all()
    serializer_class = TakeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['shot', 'is_selected', 'quality_rating']
    ordering_fields = ['take_number', 'created_at']