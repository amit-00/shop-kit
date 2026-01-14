from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.identity.domain.utils import format_validation_errors
from ..models import Seller
from ..serializers import SellerSerializer, SellerResponseSerializer
from ..utils import get_seller, check_seller_owner


class SellerViewSet(ViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow public access for retrieve action.
        """
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request: Request) -> Response:
        user = request.user
        sellers = self.queryset.filter(user=user)
        serializer = SellerResponseSerializer(sellers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        # Check if user already has a seller (OneToOneField constraint)
        if hasattr(request.user, 'seller'):
            return Response(
                {'errors': 'User is already a seller.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        # Set user from request
        serializer.save(user=request.user)
        response_serializer = SellerResponseSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        seller = get_seller(identifier)
        serializer = SellerResponseSerializer(seller)
        return Response(serializer.data)

    def update(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        seller = get_seller(identifier)

        # Check ownership
        if not check_seller_owner(seller, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(seller, data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response_serializer = SellerResponseSerializer(serializer.instance)
        return Response(response_serializer.data)

    def destroy(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        seller = get_seller(identifier)

        # Check ownership
        if not check_seller_owner(seller, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

