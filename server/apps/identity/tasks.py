from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.identity.models import User


@shared_task
def send_magic_link_email_task(user_id: int, jti: str) -> None:
    """
    Celery task to send magic link email asynchronously.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # User was deleted, skip sending email
        return

    base_url = getattr(settings, 'MAGIC_LINK_BASE_URL', 'http://localhost:8000')
    magic_link_url = f"{base_url}/api/identity/auth/verify?jti={jti}"
    
    subject = 'Sign in to your account'
    
    # Try to render HTML template, fallback to plain text
    try:
        message = render_to_string('identity/magic_link_email.html', {
            'user': user,
            'magic_link_url': magic_link_url,
            'expiry_minutes': getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30),
        })
        html_message = message
        plain_message = f"Click the following link to sign in: {magic_link_url}\n\nThis link will expire in {getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30)} minutes."
    except Exception:
        # Fallback if template doesn't exist
        html_message = None
        plain_message = f"Click the following link to sign in: {magic_link_url}\n\nThis link will expire in {getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30)} minutes."
    
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

