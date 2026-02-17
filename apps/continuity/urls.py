"""
Continuity API URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContinuityNoteViewSet

router = DefaultRouter()
router.register(r'continuity', ContinuityNoteViewSet, basename='continuity-note')

urlpatterns = [
    path('', include(router.urls)),
]