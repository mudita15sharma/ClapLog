"""
Main API URL configuration for ClapLog.
Combines all app API URLs.
"""

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet
from apps.productions.views import ProductionViewSet
from apps.scenes.views import SceneViewSet
from apps.shots.views import ShotViewSet
from apps.call_sheets.views import CallSheetViewSet
from apps.continuity.views import ContinuityNoteViewSet
from apps.props.views import PropViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'productions', ProductionViewSet, basename='production')
router.register(r'scenes', SceneViewSet, basename='scene')
router.register(r'shots', ShotViewSet, basename='shot')
router.register(r'call-sheets', CallSheetViewSet, basename='callsheet')
router.register(r'continuity-notes', ContinuityNoteViewSet, basename='continuitynote')
router.register(r'props', PropViewSet, basename='prop')

urlpatterns = [

    path('', include(router.urls)),

    # JWT Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # App APIs
    path('', include('apps.users.urls')),
    path('', include('apps.productions.urls')),
    path('', include('apps.scenes.urls')),
    path('', include('apps.shots.urls')),
    path('', include('apps.call_sheets.urls')),
    path('', include('apps.continuity.urls')),
    path('', include('apps.props.urls')),

]