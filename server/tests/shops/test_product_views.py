from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.identity.models import User
from apps.shops.models import Shop, Product


class ProductViewSetTests(APITestCase):
    """Test suite for ProductViewSet endpoints."""

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
        self.product1 = Product.objects.create(
            shop=self.shop,
            name="Product One",
            description="First product",
            sku="PROD-001",
            stock=10,
            is_published=True
        )
        
        self.product2 = Product.objects.create(
            shop=self.shop,
            name="Product Two",
            description="Second product",
            sku="PROD-002",
            stock=5,
            is_published=False
        )
        
        self.product3 = Product.objects.create(
            shop=self.shop,
            name="Another Product",
            description="Third product",
            sku="PROD-003",
            stock=20,
            is_published=True
        )

    # List Endpoint Tests
    def test_list_without_authentication(self):
        """Test list endpoint allows public access."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_filters_by_name(self):
        """Test list endpoint filters products by name."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'name': 'Product One'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Product One')

    def test_list_filters_by_sku(self):
        """Test list endpoint filters products by SKU."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'sku': 'PROD-002'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sku'], 'PROD-002')

    def test_list_filters_by_is_published_true(self):
        """Test list endpoint filters products by is_published=True."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'is_published': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for product in response.data:
            self.assertTrue(Product.objects.get(id=product['id']).is_published)

    def test_list_filters_by_is_published_false(self):
        """Test list endpoint filters products by is_published=False."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'is_published': 'false'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertFalse(Product.objects.get(id=response.data[0]['id']).is_published)

    def test_list_sorts_by_name_asc(self):
        """Test list endpoint sorts products by name ascending."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'sort': 'name', 'order': 'asc'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [p['name'] for p in response.data]
        self.assertEqual(names, sorted(names))

    def test_list_sorts_by_name_desc(self):
        """Test list endpoint sorts products by name descending."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'sort': 'name', 'order': 'desc'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [p['name'] for p in response.data]
        self.assertEqual(names, sorted(names, reverse=True))

    def test_list_sorts_by_created_at_desc(self):
        """Test list endpoint sorts products by created_at descending by default."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be sorted by created_at desc (newest first)
        created_ats = [Product.objects.get(id=p['id']).created_at for p in response.data]
        self.assertEqual(created_ats, sorted(created_ats, reverse=True))

    def test_list_applies_limit(self):
        """Test list endpoint applies limit to results."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'limit': '2'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 2)

    def test_list_with_invalid_sort_field(self):
        """Test list endpoint defaults to created_at for invalid sort field."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url, {'sort': 'invalid_field'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should still return results sorted by created_at

    def test_list_returns_only_shop_products(self):
        """Test list endpoint returns only products for the specified shop."""
        # Create product in other shop
        Product.objects.create(
            shop=self.other_shop,
            name="Other Shop Product",
            description="Product in other shop",
            sku="OTHER-001"
        )
        
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for product in response.data:
            product_obj = Product.objects.get(id=product['id'])
            self.assertEqual(product_obj.shop, self.shop)

    # Create Endpoint Tests
    def test_create_with_valid_data(self):
        """Test create endpoint with valid data creates product."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'sku': 'NEW-001',
            'stock': 15,
            'is_published': True
        }
        
        product_count_before = Product.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['sku'], data['sku'])
        
        # Verify database side effects
        self.assertEqual(Product.objects.count(), product_count_before + 1)
        product = Product.objects.get(sku=data['sku'])
        self.assertEqual(product.shop, self.shop)

    def test_create_with_ownership_check(self):
        """Test create endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'Hacked Product',
            'description': 'Unauthorized product',
            'sku': 'HACK-001',
            'stock': 1
        }
        
        product_count_before = Product.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify product was not created
        self.assertEqual(Product.objects.count(), product_count_before)

    def test_create_with_missing_required_fields(self):
        """Test create endpoint with missing required fields returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'Incomplete Product'
            # Missing description and sku
        }
        
        product_count_before = Product.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        self.assertEqual(Product.objects.count(), product_count_before)

    def test_create_without_authentication(self):
        """Test create endpoint requires authentication."""
        url = reverse('product-list', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'sku': 'NEW-001',
            'stock': 15
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Retrieve Endpoint Tests
    def test_retrieve_with_valid_product_id(self):
        """Test retrieve endpoint with valid product ID."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product1.id)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_retrieve_without_authentication(self):
        """Test retrieve endpoint allows public access."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_with_invalid_product_id_format(self):
        """Test retrieve endpoint with invalid product ID format returns 400."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid product ID.')

    def test_retrieve_with_nonexistent_product(self):
        """Test retrieve endpoint with non-existent product returns 404."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': '99999'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_product_from_different_shop(self):
        """Test retrieve endpoint returns 404 for product from different shop."""
        other_product = Product.objects.create(
            shop=self.other_shop,
            name="Other Shop Product",
            description="Product in other shop",
            sku="OTHER-001"
        )
        
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(other_product.id)
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update Endpoint Tests
    def test_update_with_valid_data(self):
        """Test update endpoint with valid data updates product."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        data = {
            'name': 'Updated Product Name',
            'description': 'Updated description',
            'sku': self.product1.sku,
            'stock': 25,
            'is_published': False
        }
        
        original_updated_at = self.product1.updated_at
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['stock'], data['stock'])
        
        # Verify database side effects
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, data['name'])
        self.assertEqual(self.product1.stock, data['stock'])
        self.assertGreater(self.product1.updated_at, original_updated_at)

    def test_update_with_ownership_check(self):
        """Test update endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        data = {
            'name': 'Hacked Product',
            'description': 'Unauthorized update',
            'sku': self.product1.sku,
            'stock': 0
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        
        # Verify product was not updated
        self.product1.refresh_from_db()
        self.assertNotEqual(self.product1.name, data['name'])

    def test_update_with_invalid_product_id_format(self):
        """Test update endpoint with invalid product ID format returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id'
        })
        data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'sku': 'UPD-001',
            'stock': 10
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid product ID.')

    def test_update_with_validation_errors(self):
        """Test update endpoint with validation errors returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        data = {
            'name': '',  # Invalid: empty name
            'description': '',  # Invalid: empty description
            'sku': '',  # Invalid: empty sku
            'stock': 10
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})

    def test_update_without_authentication(self):
        """Test update endpoint requires authentication."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'sku': self.product1.sku,
            'stock': 10
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Destroy Endpoint Tests
    def test_destroy_with_valid_product(self):
        """Test destroy endpoint with valid product deletes product."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        product_id = self.product1.id
        
        product_count_before = Product.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.assertEqual(Product.objects.count(), product_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Product.objects.get(id=product_id)

    def test_destroy_with_ownership_check(self):
        """Test destroy endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        
        product_count_before = Product.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        
        # Verify product was not deleted
        self.assertEqual(Product.objects.count(), product_count_before)
        self.assertTrue(Product.objects.filter(id=self.product1.id).exists())

    def test_destroy_with_invalid_product_id_format(self):
        """Test destroy endpoint with invalid product ID format returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': 'invalid-id'
        })
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid product ID.')

    def test_destroy_without_authentication(self):
        """Test destroy endpoint requires authentication."""
        url = reverse('product-detail', kwargs={
            'identifier': self.shop.slug,
            'product_id': str(self.product1.id)
        })
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

