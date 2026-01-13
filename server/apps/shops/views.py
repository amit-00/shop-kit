from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.identity.domain.utils import format_validation_errors
from .models import Shop, Product, Price
from .serializers import (
    ShopSerializer,
    ShopResponseSerializer,
    ProductSerializer,
    ProductResponseSerializer,
    PriceSerializer,
    PriceResponseSerializer,
)
from .utils import get_shop, check_shop_owner


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


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow public access for list and retrieve actions.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(shop=shop)
        response_serializer = ProductResponseSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        shop = get_shop(identifier)
        products = self.queryset.filter(shop=shop)

        # Apply filters
        name = request.query_params.get('name')
        if name:
            products = products.filter(name__icontains=name)

        sku = request.query_params.get('sku')
        if sku:
            products = products.filter(sku=sku)

        is_published = request.query_params.get('is_published')
        if is_published is not None:
            is_published_bool = is_published.lower() in ('true', '1', 'yes')
            products = products.filter(is_published=is_published_bool)

        # Apply sorting
        sort_field = request.query_params.get('sort', 'created_at')
        order = request.query_params.get('order', 'desc')

        # Validate sort field
        valid_sort_fields = ['name', 'sku', 'created_at', 'updated_at']
        if sort_field not in valid_sort_fields:
            sort_field = 'created_at'

        # Apply ordering
        if order == 'asc':
            products = products.order_by(sort_field)
        else:
            products = products.order_by(f'-{sort_field}')

        # Apply limit
        limit = request.query_params.get('limit', 20)
        try:
            limit = int(limit)
            if limit > 0:
                products = products[:limit]
        except (ValueError, TypeError):
            pass

        serializer = ProductResponseSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        shop = get_shop(identifier)
        try:
            product_id_int = int(product_id)
            product = get_object_or_404(self.queryset, id=product_id_int, shop=shop)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid product ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductResponseSerializer(product)
        return Response(serializer.data)

    def update(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            product_id_int = int(product_id)
            product = get_object_or_404(self.queryset, id=product_id_int, shop=shop)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid product ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(product, data=request.data)

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        response_serializer = ProductResponseSerializer(serializer.instance)
        return Response(response_serializer.data)

    def destroy(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            product_id_int = int(product_id)
            product = get_object_or_404(self.queryset, id=product_id_int, shop=shop)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Invalid product ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def _get_product(self, shop: Shop, product_id: str) -> Product:
        """
        Get product by ID, ensuring it belongs to the shop.
        """
        try:
            product_id_int = int(product_id)
            return get_object_or_404(Product.objects.filter(shop=shop), id=product_id_int)
        except (ValueError, TypeError):
            from django.http import Http404
            raise Http404('Invalid product ID.')

    def list(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        shop = get_shop(identifier)
        product = self._get_product(shop, product_id)
        prices = self.queryset.filter(product=product)

        serializer = PriceResponseSerializer(prices, many=True)
        return Response(serializer.data)

    def create(self, request: Request, **kwargs) -> Response:
        identifier = kwargs.get('identifier')
        product_id = kwargs.get('product_id')
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self._get_product(shop, product_id)
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
        shop = get_shop(identifier)
        product = self._get_product(shop, product_id)

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
        shop = get_shop(identifier)

        # Check ownership
        if not check_shop_owner(shop, request.user):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        product = self._get_product(shop, product_id)

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
