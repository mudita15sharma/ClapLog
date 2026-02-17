"""
User models for ClapLog authentication system.
Custom user model with role-based permissions.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import secrets


class UserManager(BaseUserManager):
    """
    Custom user manager for ClapLog user model.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and save a regular user with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and save a superuser with the given email, username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for ClapLog.
    Supports role-based access control for film production teams.
    """

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('director', 'Director'),
        ('producer', 'Producer'),
        ('Assistant Director', 'Assistant Director'),
        ('Director of Photography ', 'Director of Photography'),
        ('script_supervisor', 'Script Supervisor'),
        ('crew', 'Crew Member'),
    ]

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=20, blank=True)

    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default='crew',
        db_index=True,
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
    )
    bio = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.username

    @property
    def is_director(self):
        """Check if user is a director."""
        return self.role == 'director'

    @property
    def is_producer(self):
        """Check if user is a producer."""
        return self.role == 'producer'

    @property
    def is_admin_role(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def generate_verification_token(self):
        """Generate a secure verification token."""
        self.email_verification_token = secrets.token_urlsafe(32)
        self.save()
        return self.email_verification_token

    def has_production_permission(self, production, permission_type='view'):
        """
        Check if user has specific permission for a production.

        Args:
            production: Production object
            permission_type: Type of permission ('view', 'edit', 'delete')

        Returns:
            bool: True if user has permission
        """
        if self.is_superuser or self.is_admin_role:
            return True

        if production.created_by == self:
            return True

        team_member = production.team_members.filter(user=self).first()
        if team_member:
            permissions = team_member.permissions or {}
            return permissions.get(permission_type, False)

        return False
