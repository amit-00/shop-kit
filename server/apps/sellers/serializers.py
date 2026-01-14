from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Seller, Product, Price


class SellerSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Seller.objects.all(), message='Slug already exists')]
    )

    class Meta:
        model = Seller
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'support_email',
            'logo',
            'theme',
            'content',
            'custom_domain',
            'policies',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'slug': {'required': True},
            'support_email': {'required': True},
        }


class SellerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'support_email',
            'logo',
            'theme',
            'content',
            'custom_domain',
            'policies',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'name',
            'description',
            'slug',
            'support_email',
            'logo',
            'theme',
            'content',
            'custom_domain',
            'policies',
            'is_active',
            'created_at',
            'updated_at',
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'sku',
            'stock',
            'images',
            'is_active',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'sku': {'required': True},
        }


class ProductResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'sku',
            'stock',
            'images',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'name',
            'description',
            'sku',
            'stock',
            'images',
            'created_at',
            'updated_at',
        ]


class PriceSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = Price
        fields = [
            'id',
            'product_id',
            'amount',
            'currency',
            'is_default',
            'valid_from',
            'valid_to',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'product_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'amount': {'required': True},
            'currency': {'required': True},
        }


class PriceResponseSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = Price
        fields = [
            'id',
            'product_id',
            'amount',
            'currency',
            'is_default',
            'valid_from',
            'valid_to',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'product_id',
            'amount',
            'currency',
            'is_default',
            'valid_from',
            'valid_to',
            'created_at',
            'updated_at',
        ]

