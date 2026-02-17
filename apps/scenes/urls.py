"""
Scene API URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SceneViewSet

router = DefaultRouter()
router.register(r'scenes', SceneViewSet, basename='scene')

urlpatterns = [
    path('', include(router.urls)),
]