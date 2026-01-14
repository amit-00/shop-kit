from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.identity.domain.utils import format_validation_errors
from ..models import Product, Price, Seller
from ..serializers import PriceSerializer, PriceResponseSerializer
from ..utils import get_seller, check_seller_owner


class PriceViewSet(ViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow public access for list and retrieve actions.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def _get_product(self, seller: Seller, product_id: str) -> Product:
        """
        Get product by ID, ensuring it belongs to the seller.
        """
        try:
            product_id_int = int(product_id)
            return get_object_or_404(Product.objects.filter(seller=seller), id=product_id_int)
        except (ValueError, TypeError):
            raise Http404('Invalid product ID.')

    def list(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        seller = get_seller(identifier)
        product = self._get_product(seller, product_id)
        prices = self.queryset.filter(product=product)

        serializer = PriceResponseSerializer(prices, many=True)
        return Response(serializer.data)

    def create(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        seller = get_seller(identifier)

        # Check ownership
        if not check_seller_owner(seller, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self._get_product(seller, product_id)
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(product=product)
        response_serializer = PriceResponseSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        price_id = kwargs.get('price_id')
        seller = get_seller(identifier)
        product = self._get_product(seller, product_id)

        try:
            price_id_int = int(price_id)
            price = get_object_or_404(self.queryset, id=price_id_int, product=product)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid price ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PriceResponseSerializer(price)
        return Response(serializer.data)

    def destroy(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        price_id = kwargs.get('price_id')
        seller = get_seller(identifier)

        # Check ownership
        if not check_seller_owner(seller, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self._get_product(seller, product_id)

        try:
            price_id_int = int(price_id)
            price = get_object_or_404(self.queryset, id=price_id_int, product=product)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid price ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

