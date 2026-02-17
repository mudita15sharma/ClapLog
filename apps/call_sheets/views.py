"""
Call Sheet API views.
"""
from django.db import models
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import CallSheet, CallSheetScene, CastMember, CallSheetCast
from .serializers import (
    CallSheetSerializer,
    CallSheetListSerializer,
    CallSheetSceneSerializer,
    CastMemberSerializer,
    CallSheetCastSerializer
)


class CallSheetViewSet(viewsets.ModelViewSet):
    """API endpoint for call sheets."""

    queryset = CallSheet.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['production', 'status', 'shoot_date']
    ordering_fields = ['shoot_date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return CallSheetListSerializer
        return CallSheetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(
            models.Q(production__created_by=user) |
            models.Q(production__team_members__user=user)
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish the call sheet."""
        call_sheet = self.get_object()

        if call_sheet.status == 'published':
            return Response(
                {'error': 'Call sheet is already published'},
                status=status.HTTP_400_BAD_REQUEST
            )

        call_sheet.status = 'published'
        call_sheet.published_at = timezone.now()
        call_sheet.save()

        return Response({'message': 'Call sheet published successfully'})

    @action(detail=True, methods=['post'])
    def add_scene(self, request, pk=None):
        """Add a scene to the call sheet."""
        call_sheet = self.get_object()
        data = request.data.copy()
        data['call_sheet'] = call_sheet.id

        serializer = CallSheetSceneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_cast(self, request, pk=None):
        """Add cast member to the call sheet."""
        call_sheet = self.get_object()
        data = request.data.copy()
        data['call_sheet'] = call_sheet.id

        serializer = CallSheetCastSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CastMemberViewSet(viewsets.ModelViewSet):
    """API endpoint for cast members."""

    queryset = CastMember.objects.all()
    serializer_class = CastMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['production', 'role_type']
    search_fields = ['name', 'character_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(
            models.Q(production__created_by=user) |
            models.Q(production__team_members__user=user)
        ).distinct()

        return queryset


from .serializers import CastMemberDetailSerializer


class CastMemberViewSet(viewsets.ModelViewSet):
    """API endpoint for cast members."""

    queryset = CastMember.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['production', 'role_type']
    search_fields = ['name', 'character_name']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CastMemberDetailSerializer
        return CastMemberSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(
            models.Q(production__created_by=user) |
            models.Q(production__team_members__user=user)
        ).distinct()

        return queryset