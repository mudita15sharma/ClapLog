"""
Productions API views.
Includes ProductionTeamViewSet to maintain backward compatibility.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Production
from .serializers import ProductionSerializer


class ProductionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for productions.
    Automatically includes scene_count, shot_count,
    completed_scene_count in every response.
    """
    serializer_class   = ProductionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status']
    search_fields      = ['title', 'description']
    ordering_fields    = ['created_at', 'title', 'start_date']
    ordering           = ['-created_at']

    def get_queryset(self):
        """Only return productions belonging to the current user."""
        return Production.objects.filter(
            created_by=self.request.user
        ).prefetch_related('scenes', 'scenes__shots')

    def perform_create(self, serializer):
        """Automatically set created_by to the current user."""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        GET /api/productions/{id}/statistics/
        Returns detailed stats for a single production.
        """
        production = self.get_object()
        scenes     = production.scenes.all()

        total_scenes     = scenes.count()
        completed_scenes = scenes.filter(status='completed').count()
        in_progress      = scenes.filter(status='in_progress').count()
        not_started      = scenes.filter(status='not_started').count()
        on_hold          = scenes.filter(status='on_hold').count()
        total_shots      = sum(s.shots.count() for s in scenes)
        completion_pct   = (
            round((completed_scenes / total_scenes * 100), 1)
            if total_scenes > 0 else 0
        )

        return Response({
            'production_id':         production.id,
            'title':                 production.title,
            'status':                production.status,
            'total_scenes':          total_scenes,
            'completed_scenes':      completed_scenes,
            'in_progress':           in_progress,
            'not_started':           not_started,
            'on_hold':               on_hold,
            'total_shots':           total_shots,
            'completion_percentage': completion_pct,
        })

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        PATCH /api/productions/{id}/update_status/
        Quick status update without sending all fields.
        """
        production = self.get_object()
        new_status = request.data.get('status')

        valid_statuses = [
            'development', 'pre_production', 'in_production',
            'post_production', 'completed', 'on_hold'
        ]

        if not new_status:
            return Response(
                {'error': 'status field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        production.status = new_status
        production.save()

        serializer = self.get_serializer(production)
        return Response(serializer.data)


class ProductionTeamViewSet(viewsets.ViewSet):
    """
    Stub viewset for production team members.
    Implement fully when ProductionTeam model is ready.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response([])

    def create(self, request):
        return Response(
            {'detail': 'ProductionTeam feature coming soon.'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def retrieve(self, request, pk=None):
        return Response(
            {'detail': 'ProductionTeam feature coming soon.'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def update(self, request, pk=None):
        return Response(
            {'detail': 'ProductionTeam feature coming soon.'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def destroy(self, request, pk=None):
        return Response(
            {'detail': 'ProductionTeam feature coming soon.'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )