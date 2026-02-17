"""
Shot API URLs.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShotViewSet, TakeViewSet

router = DefaultRouter()
router.register(r'shots', ShotViewSet, basename='shot')
router.register(r'takes', TakeViewSet, basename='take')

urlpatterns = [
    path('', include(router.urls)),
]