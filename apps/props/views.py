"""
Props API views.
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Prop
from .serializers import PropSerializer, PropListSerializer


class PropViewSet(viewsets.ModelViewSet):
    """API endpoint for props."""

    queryset = Prop.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['production', 'scene', 'category', 'status', 'hero_prop']
    search_fields = ['name', 'description', 'brand_model']
    ordering_fields = ['name', 'category', 'cost', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PropListSerializer
        return PropSerializer

    def get_queryset(self):
        """Filter props by user's productions."""
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(
            models.Q(production__created_by=user) |
            models.Q(production__team_members__user=user)
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update prop status."""
        prop = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Prop.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        prop.status = new_status
        prop.save()

        serializer = self.get_serializer(prop)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get props grouped by category."""
        queryset = self.filter_queryset(self.get_queryset())

        categories = {}
        for prop in queryset:
            cat = prop.get_category_display()
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(PropListSerializer(prop).data)

        return Response(categories)