from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.identity.models import User
from apps.shops.models import Shop, Product, Price


class PriceViewSetTests(APITestCase):
    """Test suite for PriceViewSet endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        # Create test users
        self.user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        
        self.other_user = User.objects.create_user(
            email="other@example.com",
            phone="0987654321",
            first_name="Jane",
            last_name="Smith"
        )
        
        # Create test shops
        self.shop = Shop.objects.create(
            user=self.user,
            name="My Shop",
            slug="my-shop",
            support_email="support@myshop.com"
        )
        
        self.other_shop = Shop.objects.create(
            user=self.other_user,
            name="Other Shop",
            slug="other-shop",
            support_email="support@othershop.com"
        )
        
        # Create test products
        self.product = Product.objects.create(
            shop=self.shop,
            name="Test Product",
            description="A test product",
            sku="TEST-001",
            stock=10
        )
        
        self.other_product = Product.objects.create(
            shop=self.other_shop,
            name="Other Product",
            description="Product in other shop",
            sku="OTHER-001",
            stock=5
        )
        
        # Create test prices
        self.price1 = Price.objects.create(
            product=self.product,
            amount=1000,
            currency=Price.Currency.USD,
            is_default=True
        )
        
        self.price2 = Price.objects.create(
            product=self.product,
            amount=1500,
            currency=Price.Currency.CAD,
            is_default=False
        )

    # List Endpoint Tests
    def test_list_without_authentication(self):
        """Test list endpoint allows public access."""
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_returns_only_product_prices(self):
        """Test list endpoint returns only prices for the specified product."""
        # Create price for other product
        Price.objects.create(
            product=self.other_product,
            amount=2000,
            currency=Price.Currency.USD
        )
        
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for price in response.data:
            price_obj = Price.objects.get(id=price['id'])
            self.assertEqual(price_obj.product, self.product)

    def test_list_with_invalid_product_id_format(self):
        """Test list endpoint with invalid product ID format raises 404."""
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_nonexistent_product(self):
        """Test list endpoint with non-existent product returns 404."""
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': '99999'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_with_product_from_different_shop(self):
        """Test list endpoint returns 404 for product from different shop."""
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.other_product.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Create Endpoint Tests
    def test_create_with_valid_data(self):
        """Test create endpoint with valid data creates price."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        data = {
            'amount': 2000,
            'currency': Price.Currency.USD,
            'is_default': False
        }
        
        price_count_before = Price.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], data['amount'])
        self.assertEqual(response.data['currency'], data['currency'])
        
        # Verify database side effects
        self.assertEqual(Price.objects.count(), price_count_before + 1)
        price = Price.objects.get(id=response.data['id'])
        self.assertEqual(price.product, self.product)

    def test_create_with_ownership_check(self):
        """Test create endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        data = {
            'amount': 3000,
            'currency': Price.Currency.USD,
            'is_default': False
        }
        
        price_count_before = Price.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify price was not created
        self.assertEqual(Price.objects.count(), price_count_before)

    def test_create_with_missing_required_fields(self):
        """Test create endpoint with missing required fields returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        data = {
            'amount': 1000
            # Missing currency
        }
        
        price_count_before = Price.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        self.assertEqual(Price.objects.count(), price_count_before)

    def test_create_without_authentication(self):
        """Test create endpoint requires authentication."""
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id)
        })
        data = {
            'amount': 2000,
            'currency': Price.Currency.USD
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_with_invalid_product_id_format(self):
        """Test create endpoint with invalid product ID format raises 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-list', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id'
        })
        data = {
            'amount': 2000,
            'currency': Price.Currency.USD
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Retrieve Endpoint Tests
    def test_retrieve_with_valid_price_id(self):
        """Test retrieve endpoint with valid price ID."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(self.price1.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.price1.id)
        self.assertEqual(response.data['amount'], self.price1.amount)
        self.assertEqual(response.data['currency'], self.price1.currency)

    def test_retrieve_without_authentication(self):
        """Test retrieve endpoint allows public access."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(self.price1.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_with_invalid_price_id_format(self):
        """Test retrieve endpoint with invalid price ID format returns 400."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': 'invalid-id'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid price ID.')

    def test_retrieve_with_nonexistent_price(self):
        """Test retrieve endpoint with non-existent price returns 404."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': '99999'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_price_from_different_product(self):
        """Test retrieve endpoint returns 404 for price from different product."""
        other_price = Price.objects.create(
            product=self.other_product,
            amount=2000,
            currency=Price.Currency.USD
        )
        
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(other_price.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_invalid_product_id_format(self):
        """Test retrieve endpoint with invalid product ID format raises 404."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id',
            'price_id': str(self.price1.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Destroy Endpoint Tests
    def test_destroy_with_valid_price(self):
        """Test destroy endpoint with valid price deletes price."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(self.price1.id)
        })
        price_id = self.price1.id
        
        price_count_before = Price.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.assertEqual(Price.objects.count(), price_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Price.objects.get(id=price_id)

    def test_destroy_with_ownership_check(self):
        """Test destroy endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(self.price1.id)
        })
        
        price_count_before = Price.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify price was not deleted
        self.assertEqual(Price.objects.count(), price_count_before)
        self.assertTrue(Price.objects.filter(id=self.price1.id).exists())

    def test_destroy_with_invalid_price_id_format(self):
        """Test destroy endpoint with invalid price ID format returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': 'invalid-id'
        })
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid price ID.')

    def test_destroy_without_authentication(self):
        """Test destroy endpoint requires authentication."""
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(self.price1.id)
        })
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_with_invalid_product_id_format(self):
        """Test destroy endpoint with invalid product ID format raises 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id',
            'price_id': str(self.price1.id)
        })
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_with_price_from_different_product(self):
        """Test destroy endpoint returns 404 for price from different product."""
        other_price = Price.objects.create(
            product=self.other_product,
            amount=2000,
            currency=Price.Currency.USD
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('price-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product.id),
            'price_id': str(other_price.id)
        })
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

