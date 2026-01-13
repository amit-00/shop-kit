from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.identity.domain.utils import format_validation_errors
from ..models import Shop
from ..serializers import ShopSerializer, ShopResponseSerializer
from ..utils import get_shop, check_shop_owner


class ShopViewSet(ViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
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
        shops = self.queryset.filter(user=user)
        serializer = ShopResponseSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        # Set user from request
        serializer.save(user=request.user)
        response_serializer = ShopResponseSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        shop = get_shop(identifier)
        serializer = ShopResponseSerializer(shop)
        return Response(serializer.data)

    def update(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(shop, data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response_serializer = ShopResponseSerializer(serializer.instance)
        return Response(response_serializer.data)

    def destroy(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

