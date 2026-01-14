from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.identity.models import User
from apps.sellers.models import Seller


class SellerViewSetTests(APITestCase):
    """Test suite for SellerViewSet endpoints."""

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

        self.user_without_seller = User.objects.create_user(
            email="userwithoutseller@example.com",
            phone="1111111111",
            first_name="User",
            last_name="Without Seller"
        )
        
        # Create test sellers
        self.seller = Seller.objects.create(
            user=self.user,
            name="My Seller",
            slug="my-seller",
            support_email="support@myseller.com",
            description="My seller description"
        )
        
        self.other_seller = Seller.objects.create(
            user=self.other_user,
            name="Other Seller",
            slug="other-seller",
            support_email="support@otherseller.com"
        )

    # List Endpoint Tests
    def test_list_with_authenticated_user(self):
        """Test list endpoint returns only user's sellers."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slug'], self.seller.slug)
        self.assertEqual(response.data[0]['name'], self.seller.name)

    def test_list_without_authentication(self):
        """Test list endpoint requires authentication."""
        url = reverse('seller-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_empty_when_user_has_no_seller(self):
        """Test list endpoint returns empty list when user has no seller."""
        # Create a user without a seller
        user_without_seller = User.objects.create_user(
            email="noseller@example.com",
            phone="7777777777",
            first_name="No",
            last_name="Seller"
        )
        
        self.client.force_authenticate(user=user_without_seller)
        url = reverse('seller-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_excludes_other_users_sellers(self):
        """Test list endpoint excludes sellers from other users."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        seller_slugs = [seller['slug'] for seller in response.data]
        self.assertIn(self.seller.slug, seller_slugs)
        self.assertNotIn(self.other_seller.slug, seller_slugs)

    # Create Endpoint Tests
    def test_create_with_valid_data(self):
        """Test create endpoint with valid data creates seller for user without seller."""
        # Create a user without a seller
        new_user = User.objects.create_user(
            email="newuser@example.com",
            phone="5555555555",
            first_name="New",
            last_name="User"
        )
        
        self.client.force_authenticate(user=new_user)
        url = reverse('seller-list')
        data = {
            'name': 'New Seller',
            'slug': 'new-seller',
            'support_email': 'support@newseller.com',
            'description': 'A new seller',
            'theme': Seller.Theme.DARK
        }
        
        seller_count_before = Seller.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['slug'], data['slug'])
        self.assertEqual(response.data['support_email'], data['support_email'])
        
        # Verify database side effects
        self.assertEqual(Seller.objects.count(), seller_count_before + 1)
        seller = Seller.objects.get(slug=data['slug'])
        self.assertEqual(seller.user, new_user)
        self.assertEqual(seller.name, data['name'])

    def test_create_sets_user_from_request(self):
        """Test create endpoint sets user from authenticated request."""
        # Create a user without a seller
        new_user = User.objects.create_user(
            email="newuser2@example.com",
            phone="6666666666",
            first_name="New",
            last_name="User2"
        )
        
        self.client.force_authenticate(user=new_user)
        url = reverse('seller-list')
        data = {
            'name': 'User Seller',
            'slug': 'user-seller',
            'support_email': 'support@userseller.com'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        seller = Seller.objects.get(slug=data['slug'])
        self.assertEqual(seller.user, new_user)

    def test_create_with_missing_required_fields(self):
        """Test create endpoint with missing required fields returns 400."""
        self.client.force_authenticate(user=self.user_without_seller)
        url = reverse('seller-list')
        data = {
            'name': 'Incomplete Seller'
            # Missing slug and support_email
        }
        
        seller_count_before = Seller.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        
        # Verify no seller was created
        self.assertEqual(Seller.objects.count(), seller_count_before)

    def test_create_with_duplicate_slug(self):
        """Test create endpoint with duplicate slug returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-list')
        data = {
            'name': 'Duplicate Seller',
            'slug': self.seller.slug,  # Already exists
            'support_email': 'support@duplicate.com'
        }
        
        seller_count_before = Seller.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Seller.objects.count(), seller_count_before)

    def test_create_without_authentication(self):
        """Test create endpoint requires authentication."""
        url = reverse('seller-list')
        data = {
            'name': 'New Seller',
            'slug': 'new-seller',
            'support_email': 'support@newseller.com'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_fails_when_user_already_has_seller(self):
        """Test create endpoint returns 400 when user already has a seller (OneToOneField constraint)."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-list')
        data = {
            'name': 'Second Seller',
            'slug': 'second-seller',
            'support_email': 'support@secondseller.com'
        }
        
        seller_count_before = Seller.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertIn('already has a seller', response.data['errors'].lower())
        
        # Verify no new seller was created
        self.assertEqual(Seller.objects.count(), seller_count_before)

    # Retrieve Endpoint Tests
    def test_retrieve_with_valid_id(self):
        """Test retrieve endpoint with valid seller ID."""
        url = reverse('seller-detail', kwargs={'identifier': str(self.seller.id)})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.seller.id)
        self.assertEqual(response.data['slug'], self.seller.slug)
        self.assertEqual(response.data['name'], self.seller.name)

    def test_retrieve_with_valid_slug(self):
        """Test retrieve endpoint with valid seller slug."""
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.seller.slug)
        self.assertEqual(response.data['id'], self.seller.id)

    def test_retrieve_without_authentication(self):
        """Test retrieve endpoint allows public access."""
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_with_nonexistent_seller(self):
        """Test retrieve endpoint with non-existent seller returns 404."""
        url = reverse('seller-detail', kwargs={'identifier': '99999'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_with_nonexistent_slug(self):
        """Test retrieve endpoint with non-existent slug returns 404."""
        url = reverse('seller-detail', kwargs={'identifier': 'non-existent-slug'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Update Endpoint Tests
    def test_update_with_valid_data(self):
        """Test update endpoint with valid data updates seller."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        data = {
            'name': 'Updated Seller Name',
            'slug': self.seller.slug,
            'support_email': 'newemail@seller.com',
            'description': 'Updated description'
        }
        
        original_updated_at = self.seller.updated_at
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['support_email'], data['support_email'])
        
        # Verify database side effects
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.name, data['name'])
        self.assertEqual(self.seller.support_email, data['support_email'])
        # Verify updated_at timestamp changed
        self.assertGreater(self.seller.updated_at, original_updated_at)

    def test_update_with_ownership_check(self):
        """Test update endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        data = {
            'name': 'Hacked Seller',
            'slug': self.seller.slug,
            'support_email': 'hacked@seller.com'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify seller was not updated
        self.seller.refresh_from_db()
        self.assertNotEqual(self.seller.name, data['name'])

    def test_update_with_validation_errors(self):
        """Test update endpoint with validation errors returns 400."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        data = {
            'name': '',  # Invalid: empty name
            'slug': self.seller.slug,
            'support_email': 'invalid-email'  # Invalid email format
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})

    def test_update_without_authentication(self):
        """Test update endpoint requires authentication."""
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        data = {
            'name': 'Updated Seller',
            'slug': self.seller.slug,
            'support_email': 'support@seller.com'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Destroy Endpoint Tests
    def test_destroy_with_valid_seller(self):
        """Test destroy endpoint with valid seller deletes seller."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        seller_id = self.seller.id
        
        seller_count_before = Seller.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.assertEqual(Seller.objects.count(), seller_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Seller.objects.get(id=seller_id)

    def test_destroy_with_ownership_check(self):
        """Test destroy endpoint checks ownership and returns 403 for non-owner."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        
        seller_count_before = Seller.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )
        
        # Verify seller was not deleted
        self.assertEqual(Seller.objects.count(), seller_count_before)
        self.assertTrue(Seller.objects.filter(id=self.seller.id).exists())

    def test_destroy_without_authentication(self):
        """Test destroy endpoint requires authentication."""
        url = reverse('seller-detail', kwargs={'identifier': self.seller.slug})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_with_nonexistent_seller(self):
        """Test destroy endpoint with non-existent seller returns 404."""
        self.client.force_authenticate(user=self.user)
        url = reverse('seller-detail', kwargs={'identifier': '99999'})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

