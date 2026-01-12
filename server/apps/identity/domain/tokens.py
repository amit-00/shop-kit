import secrets
from typing import Optional
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.redis import store_magic_link_jti, get_magic_link_jti, delete_magic_link_jti
from apps.identity.models import User


def mint_jwt_pair(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def generate_magic_link_jti() -> str:
    """
    Creates a JTI (JWT ID) for the magic link.
    """
    return secrets.token_urlsafe(32)


def generate_magic_link_email_content(user: User, jti: str) -> tuple[str, str]:
    """
    Generates the HTML and plain text content for the magic link email.
    """
    base_url = getattr(settings, 'MAGIC_LINK_BASE_URL', 'http://localhost:8000')
    magic_link_url = f"{base_url}/api/identity/auth/verify?jti={jti}"
        
    try:
        message = render_to_string('identity/magic_link_email.html', {
            'user': user,
            'magic_link_url': magic_link_url,
            'expiry_minutes': getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30),
        })
        html_message = message
    except Exception:
        html_message = None

    plain_message = (
        f"Click the following link to sign in: {magic_link_url}\n\n"
        f"This link will expire in {getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30)} minutes."
    )
    
    return html_message, plain_message


def send_magic_link_email(user: User, jti: str) -> None:
    """
    Sends email with magic link containing JTI.
    """
    
    subject = 'ShopFast - Login to your account'
    
    html_message, plain_message = generate_magic_link_email_content(user, jti)
    
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def verify_magic_link_jti(jti: str) -> Optional[User]:
    """
    Validates and retrieves user from JTI token.
    """
    user_id = get_magic_link_jti(jti)
    
    if not user_id:
        return None
    
    try:
        user = User.objects.get(id=user_id)
        delete_magic_link_jti(jti)
        return user
    except User.DoesNotExist:
        delete_magic_link_jti(jti)
        return None