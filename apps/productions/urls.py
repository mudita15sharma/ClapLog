"""
Productions URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionViewSet

router = DefaultRouter()
router.register(r'productions', ProductionViewSet, basename='production')

urlpatterns = [
    path('', include(router.urls)),
]