from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.identity.domain.utils import format_validation_errors
from apps.identity.domain.tokens import (
    generate_magic_link_jti,
    verify_magic_link_jti,
    mint_jwt_pair,
)
from apps.identity.models import User
from apps.identity.serializers import (
    LoginRequestSerializer,
    RegisterRequestSerializer,
    MagicLinkVerifySerializer,
    TokenResponseSerializer,
)
from apps.identity.tasks import send_magic_link_email_task
from apps.common.redis import store_magic_link_jti


class LoginRequestView(APIView):
    """
    View to request a magic link for email-based authentication.
    Only works for existing users.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginRequestSerializer(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response(
                {'errors': formatted_errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']

        # Get existing user - do not create
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'No account found with this email. Please register first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate JTI
        jti = generate_magic_link_jti()

        # Store JTI in Redis with TTL
        ttl_seconds = getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30) * 60
        store_magic_link_jti(jti, str(user.id), ttl_seconds)

        # Send email with magic link asynchronously using Celery
        send_magic_link_email_task.delay(user.id, jti)

        # Return success response immediately (email is sent asynchronously)
        return Response(
            {'message': 'Magic link sent to your email. Please check your inbox.'},
            status=status.HTTP_200_OK
        )


class RegisterRequestView(APIView):
    """
    View to register a new user and send a magic link for email verification.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterRequestSerializer(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response(
                {'errors': formatted_errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'An account with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new user
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Generate JTI
        jti = generate_magic_link_jti()

        # Store JTI in Redis with TTL
        ttl_seconds = getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 30) * 60
        store_magic_link_jti(jti, str(user.id), ttl_seconds)

        # Send email with magic link asynchronously using Celery
        send_magic_link_email_task.delay(user.id, jti)

        # Return success response immediately (email is sent asynchronously)
        return Response(
            {'message': 'Account created. Magic link sent to your email. Please check your inbox.'},
            status=status.HTTP_201_CREATED
        )


class MagicLinkVerifyView(APIView):
    """
    View to verify magic link JTI and issue JWT tokens.
    Supports both GET (for browser clicks) and POST requests.
    """
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Handle GET requests from magic link clicks."""
        jti = request.query_params.get('jti')

        if not jti:
            return Response(
                {'error': 'JTI parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return self._verify_and_issue_tokens(jti)

    def post(self, request: Request) -> Response:
        """Handle POST requests with JTI in body."""
        serializer = MagicLinkVerifySerializer(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response(
                {'errors': formatted_errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        jti = serializer.validated_data['jti']
        return self._verify_and_issue_tokens(jti)

    def _verify_and_issue_tokens(self, jti: str) -> Response:
        """Common logic to verify JTI and issue tokens."""
        # Verify JTI and get user
        user = verify_magic_link_jti(jti)

        if not user:
            return Response(
                {'error': 'Invalid or expired magic link. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Issue JWT tokens
        tokens = mint_jwt_pair(user)

        # Return tokens
        response_serializer = TokenResponseSerializer(tokens)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

