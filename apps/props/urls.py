"""
Props URL configuration.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropViewSet

router = DefaultRouter()
router.register(r'props', PropViewSet, basename='prop')

urlpatterns = [
    path('', include(router.urls)),
]