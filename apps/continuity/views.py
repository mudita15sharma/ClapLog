from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import ContinuityNote
from .serializers import ContinuityNoteSerializer


class ContinuityNoteViewSet(viewsets.ModelViewSet):
    """API endpoint for continuity notes."""

    queryset = ContinuityNote.objects.all()
    serializer_class = ContinuityNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scene', 'category', 'severity', 'status']
    search_fields = ['description', 'warnings', 'actor_character']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter by production if specified."""
        queryset = super().get_queryset()
        production_id = self.request.query_params.get('production')

        if production_id:
            queryset = queryset.filter(scene__production_id=production_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """Override create to add better error logging."""
        print("=" * 50)
        print("CONTINUITY NOTE CREATE REQUEST")
        print("Data received:", request.data)
        print("=" * 50)
        return super().create(request, *args, **kwargs)
