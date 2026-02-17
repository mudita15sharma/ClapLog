"""
Email service for user verification and notifications.
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_verification_email(user, verification_url):
    """
    Send email verification to user.

    Args:
        user: User instance
        verification_url: Full URL for email verification
    """

    subject = 'Verify your ClapLog account'

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
                border-bottom: 3px solid #daa520;
            }}
            .header h1 {{
                color: #8b0000;
                margin: 0;
            }}
            .content {{
                padding: 30px 0;
            }}
            .button {{
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #8b0000 0%, #a00000 100%);
                color: #fff !important;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 12px;
            }}
            .token {{
                background: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                word-break: break-all;
                font-family: monospace;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 ClapLog</h1>
                <p>Film Production Tracker</p>
            </div>

            <div class="content">
                <h2>Welcome, {user.first_name or user.username}!</h2>
                <p>Thank you for registering with ClapLog. To complete your registration and start tracking your film productions, please verify your email address.</p>

                <p style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </p>

                <p>If the button doesn't work, copy and paste this link into your browser:</p>
                <div class="token">{verification_url}</div>

                <p><strong>This link will expire in 24 hours.</strong></p>

                <p>If you didn't create an account with ClapLog, please ignore this email.</p>
            </div>

            <div class="footer">
                <p>ClapLog - Track your vision, frame by frame</p>
                <p>&copy; 2026 ClapLog. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    Welcome to ClapLog!

    Hi {user.first_name or user.username},

    Thank you for registering with ClapLog. To complete your registration, please verify your email address by clicking the link below:

    {verification_url}

    This link will expire in 24 hours.

    If you didn't create an account with ClapLog, please ignore this email.

    Best regards,
    The ClapLog Team
    """

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
        return False


def send_welcome_email(user):
    """Send welcome email after verification."""

    subject = 'Welcome to ClapLog! 🎬'

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h1 style="color: #8b0000;">🎉 Welcome to ClapLog!</h1>
            <p>Hi {user.first_name or user.username},</p>
            <p>Your email has been verified successfully! You can now log in and start managing your film productions.</p>
            <p>Get started by:</p>
            <ul>
                <li>Creating your first production</li>
                <li>Breaking down scenes</li>
                <li>Planning shots</li>
                <li>Generating call sheets</li>
            </ul>
            <p>Happy filmmaking!</p>
            <p>The ClapLog Team</p>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    Welcome to ClapLog!

    Hi {user.first_name or user.username},

    Your email has been verified successfully! You can now log in and start managing your film productions.

    Happy filmmaking!
    The ClapLog Team
    """

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")