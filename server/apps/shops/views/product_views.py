from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.identity.domain.utils import format_validation_errors
from ..models import Product
from ..serializers import ProductSerializer, ProductResponseSerializer
from ..utils import get_shop, check_shop_owner


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

