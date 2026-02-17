"""
Call Sheet API URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CallSheetViewSet, CastMemberViewSet

router = DefaultRouter()
router.register(r'call-sheets', CallSheetViewSet, basename='call-sheet')
router.register(r'cast-members', CastMemberViewSet, basename='cast-member')

urlpatterns = [
    path('', include(router.urls)),
]