from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.identity.models import User
from apps.shops.models import Shop


class ShopViewSetTests(APITestCase):
    """Test suite for ShopViewSet endpoints."""

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
            support_email="support@myshop.com",
            description="My shop description"
        )
        
        self.other_shop = Shop.objects.create(
            user=self.other_user,
            name="Other Shop",
            slug="other-shop",
            support_email="support@othershop.com"
        )

    # List Endpoint Tests
    def test_list_with_authenticated_user(self):
        """Test list endpoint returns only user's shops."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slug'], self.shop.slug)
        self.assertEqual(response.data[0]['name'], self.shop.name)

    def test_list_without_authentication(self):
        """Test list endpoint requires authentication."""
        url = reverse('shop-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_excludes_other_users_shops(self):
        """Test list endpoint excludes shops from other users."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shop_slugs = [shop['slug'] for shop in response.data]
        self.assertIn(self.shop.slug, shop_slugs)
        self.assertNotIn(self.other_shop.slug, shop_slugs)

    # Create Endpoint Tests
    def test_create_with_valid_data(self):
        """Test create endpoint with valid data creates shop."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        data = {
            'name': 'New Shop',
            'slug': 'new-shop',
            'support_email': 'support@newshop.com',
            'description': 'A new shop',
            'theme': Shop.Theme.DARK
        }
        
        shop_count_before = Shop.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['slug'], data['slug'])
        self.assertEqual(response.data['support_email'], data['support_email'])
        
        # Verify database side effects
        self.assertEqual(Shop.objects.count(), shop_count_before + 1)
        shop = Shop.objects.get(slug=data['slug'])
        self.assertEqual(shop.user, self.user)
        self.assertEqual(shop.name, data['name'])

    def test_create_sets_user_from_request(self):
        """Test create endpoint sets user from authenticated request."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        data = {
            'name': 'User Shop',
            'slug': 'user-shop',
            'support_email': 'support@usershop.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        shop = Shop.objects.get(slug=data['slug'])
        self.assertEqual(shop.user, self.user)

    def test_create_with_missing_required_fields(self):
        """Test create endpoint with missing required fields returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        data = {
            'name': 'Incomplete Shop'
            # Missing slug and support_email
        }
        
        shop_count_before = Shop.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        
        # Verify no shop was created
        self.assertEqual(Shop.objects.count(), shop_count_before)

    def test_create_with_duplicate_slug(self):
        """Test create endpoint with duplicate slug returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-list')
        data = {
            'name': 'Duplicate Shop',
            'slug': self.shop.slug,  # Already exists
            'support_email': 'support@duplicate.com'
        }
        
        shop_count_before = Shop.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Shop.objects.count(), shop_count_before)

    def test_create_without_authentication(self):
        """Test create endpoint requires authentication."""
        url = reverse('shop-list')
        data = {
            'name': 'New Shop',
            'slug': 'new-shop',
            'support_email': 'support@newshop.com'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Retrieve Endpoint Tests
    def test_retrieve_with_valid_id(self):
        """Test retrieve endpoint with valid shop ID."""
        url = reverse('shop-detail', kwargs={'identifier': str(self.shop.id)})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.shop.id)
        self.assertEqual(response.data['slug'], self.shop.slug)
        self.assertEqual(response.data['name'], self.shop.name)

    def test_retrieve_with_valid_slug(self):
        """Test retrieve endpoint with valid shop slug."""
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.shop.slug)
        self.assertEqual(response.data['id'], self.shop.id)

    def test_retrieve_without_authentication(self):
        """Test retrieve endpoint allows public access."""
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_with_nonexistent_shop(self):
        """Test retrieve endpoint with non-existent shop returns 404."""
        url = reverse('shop-detail', kwargs={'identifier': '99999'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_nonexistent_slug(self):
        """Test retrieve endpoint with non-existent slug returns 404."""
        url = reverse('shop-detail', kwargs={'identifier': 'non-existent-slug'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update Endpoint Tests
    def test_update_with_valid_data(self):
        """Test update endpoint with valid data updates shop."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'Updated Shop Name',
            'slug': self.shop.slug,
            'support_email': 'newemail@shop.com',
            'description': 'Updated description'
        }
        
        original_updated_at = self.shop.updated_at
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['support_email'], data['support_email'])
        
        # Verify database side effects
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, data['name'])
        self.assertEqual(self.shop.support_email, data['support_email'])
        # Verify updated_at timestamp changed
        self.assertGreater(self.shop.updated_at, original_updated_at)

    def test_update_with_ownership_check(self):
        """Test update endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'Hacked Shop',
            'slug': self.shop.slug,
            'support_email': 'hacked@shop.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify shop was not updated
        self.shop.refresh_from_db()
        self.assertNotEqual(self.shop.name, data['name'])

    def test_update_with_validation_errors(self):
        """Test update endpoint with validation errors returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        data = {
            'name': '',  # Invalid: empty name
            'slug': self.shop.slug,
            'support_email': 'invalid-email'  # Invalid email format
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})

    def test_update_without_authentication(self):
        """Test update endpoint requires authentication."""
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        data = {
            'name': 'Updated Shop',
            'slug': self.shop.slug,
            'support_email': 'support@shop.com'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Destroy Endpoint Tests
    def test_destroy_with_valid_shop(self):
        """Test destroy endpoint with valid shop deletes shop."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        shop_id = self.shop.id
        
        shop_count_before = Shop.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.assertEqual(Shop.objects.count(), shop_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Shop.objects.get(id=shop_id)

    def test_destroy_with_ownership_check(self):
        """Test destroy endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        
        shop_count_before = Shop.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify shop was not deleted
        self.assertEqual(Shop.objects.count(), shop_count_before)
        self.assertTrue(Shop.objects.filter(id=self.shop.id).exists())

    def test_destroy_without_authentication(self):
        """Test destroy endpoint requires authentication."""
        url = reverse('shop-detail', kwargs={'identifier': self.shop.slug})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_with_nonexistent_shop(self):
        """Test destroy endpoint with non-existent shop returns 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('shop-detail', kwargs={'identifier': '99999'})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

