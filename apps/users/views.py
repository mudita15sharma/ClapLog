"""
User API views for ClapLog.
Handles user registration, authentication, and profile management.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Set permissions based on action.
        - create (register): Allow anyone
        - verify_email: Allow anyone
        - resend_verification: Allow anyone
        - everything else: Require authentication
        """
        if self.action in ['create', 'verify_email', 'resend_verification']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        Register a new user.
        Public endpoint - no authentication required.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'User registered successfully! Please check your email to verify your account.'
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current authenticated user's information.

        GET /api/users/me/
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """
        Verify email with token.
        PUBLIC ENDPOINT - No authentication required.

        POST /api/users/verify_email/
        Body: {"token": "verification_token"}
        """
        token = request.data.get('token')

        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email_verification_token=token)

            if user.email_verified:
                return Response({
                    'message': 'Email already verified',
                    'email': user.email
                })

            user.email_verified = True
            user.email_verification_token = ''
            user.is_active = True
            user.save()

            try:
                from .email_service import send_welcome_email
                send_welcome_email(user)
            except Exception as e:
                print(f"Failed to send welcome email: {e}")

            return Response({
                'message': 'Email verified successfully! You can now log in.',
                'email': user.email
            })

        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_verification(self, request):
        """
        Resend verification email.
        PUBLIC ENDPOINT - No authentication required.

        POST /api/users/resend_verification/
        Body: {"email": "user@example.com"}
        """
        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)

            if user.email_verified:
                return Response(
                    {'message': 'Email already verified'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = user.generate_verification_token()

            verification_url = f"{settings.FRONTEND_URL}/?verify_email={token}"

            from .email_service import send_verification_email
            try:
                if send_verification_email(user, verification_url):
                    return Response({
                        'message': 'Verification email sent! Please check your inbox.'
                    })
                else:
                    return Response(
                        {'error': 'Failed to send email. Please try again later.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            except Exception as e:
                print(f"Email send error: {e}")
                return Response(
                    {'error': 'Failed to send email. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except User.DoesNotExist:
            return Response({
                'message': 'If that email exists, a verification email has been sent.'
            })

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user's profile."""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(request.user).data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')

        if not old_password or not new_password or not new_password2:
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != new_password2:
            return Response(
                {'error': 'New passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {'error': 'Password must be at least 8 characters long'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({
            'message': 'Password changed successfully'
        })