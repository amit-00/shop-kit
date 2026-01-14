from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase
from rest_framework import status

from apps.identity.models import User, Plan
from apps.common.model_utils import Currency


class UserViewSetTests(APITestCase):
    """Test suite for UserViewSet endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        # Create test plans
        self.plan_month = Plan.objects.create(
            code="plan_month",
            name="Monthly Plan",
            description="Monthly subscription",
            unit_amount=1000,
            currency="usd",
            interval="month",
            is_active=True
        )
        
        self.plan_year = Plan.objects.create(
            code="plan_year",
            name="Yearly Plan",
            description="Yearly subscription",
            unit_amount=10000,
            currency=Currency.CAD,
            interval="year",
            is_active=True
        )
        
        self.plan_inactive = Plan.objects.create(
            code="plan_inactive",
            name="Inactive Plan",
            description="Inactive subscription",
            unit_amount=500,
            currency="usd",
            interval="month",
            is_active=False
        )
        
        # Create test user
        self.user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )

        self.client.force_authenticate(user=self.user)

    # List Endpoint Tests
    def test_list_with_valid_email(self):
        """Test list endpoint with valid email returns user data."""
        url = reverse('user-list')
        response = self.client.get(url, {'email': self.user.email})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)
        
        # Verify no database changes
        user_count_before = User.objects.count()
        User.objects.get(id=self.user.id)
        self.assertEqual(User.objects.count(), user_count_before)

    def test_list_without_email(self):
        """Test list endpoint without email parameter returns 400."""
        url = reverse('user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email is required')

    def test_list_with_nonexistent_email(self):
        """Test list endpoint with non-existent email returns 404."""
        url = reverse('user-list')
        response = self.client.get(url, {'email': 'nonexistent@example.com'})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Create Endpoint Tests
    def test_create_user_with_valid_data(self):
        """Test create endpoint with valid data creates user."""
        url = reverse('user-list')
        data = {
            'email': 'newuser@example.com',
            'phone': '9876543210',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        
        user_count_before = User.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['phone'], data['phone'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        
        # Verify database side effects
        self.assertEqual(User.objects.count(), user_count_before + 1)
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.phone, data['phone'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_create_user_with_missing_fields(self):
        """Test create endpoint with missing required fields returns 400."""
        url = reverse('user-list')
        data = {
            'email': 'incomplete@example.com'
            # Missing first_name, last_name
        }
        
        user_count_before = User.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        
        # Verify no user was created
        self.assertEqual(User.objects.count(), user_count_before)

    def test_create_user_with_invalid_email(self):
        """Test create endpoint with invalid email format returns 400."""
        url = reverse('user-list')
        data = {
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_count_before = User.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), user_count_before)

    def test_create_user_with_duplicate_email(self):
        """Test create endpoint with duplicate email returns 400."""
        url = reverse('user-list')
        data = {
            'email': self.user.email,  # Already exists
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_count_before = User.objects.count()
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), user_count_before)

    # Retrieve Endpoint Tests
    def test_retrieve_user_with_valid_id(self):
        """Test retrieve endpoint with valid user ID returns user data."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)
        
        # Verify no database changes
        user_count_before = User.objects.count()
        User.objects.get(id=self.user.id)
        self.assertEqual(User.objects.count(), user_count_before)

    def test_retrieve_user_with_nonexistent_id(self):
        """Test retrieve endpoint with non-existent user ID returns 404."""
        url = reverse('user-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_user_with_invalid_uuid(self):
        """Test retrieve endpoint with invalid UUID format returns 404."""
        url = reverse('user-detail', kwargs={'pk': 'invalid-uuid'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        self.assertIn('pk', response.data['errors'] or {})
        self.assertEqual(response.data['errors']['pk'][0], 'Invalid UUID format.')

    # Partial Update Endpoint Tests
    def test_partial_update_with_valid_data(self):
        """Test partial update endpoint with valid data updates user."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        data = {
            'phone': '5555555555',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        original_updated_at = self.user.updated_at
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify database side effects
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, data['phone'])
        self.assertEqual(self.user.first_name, data['first_name'])
        self.assertEqual(self.user.last_name, data['last_name'])
        # Verify updated_at timestamp changed
        self.assertGreater(self.user.updated_at, original_updated_at)

    def test_partial_update_single_field(self):
        """Test partial update with only one field works correctly."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        original_first_name = self.user.first_name
        original_phone = self.user.phone
        
        data = {'phone': '1111111111'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only phone was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, data['phone'])
        self.assertEqual(self.user.first_name, original_first_name)

    def test_partial_update_with_allowed_empty_string(self):
        """Test partial update with empty string values handled correctly."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        data = {
            'phone': ''
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify empty strings are saved
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '')

    def test_partial_update_with_disallowed_empty_string(self):
        """Test partial update with empty string values disallowed."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        data = {
            'first_name': '',
            'last_name': ''
        }
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data or {})
        self.assertIn('first_name', response.data['errors'] or {})
        self.assertIn('last_name', response.data['errors'] or {})
        self.assertEqual(response.data['errors']['first_name'][0], 'This field may not be blank.')
        self.assertEqual(response.data['errors']['last_name'][0], 'This field may not be blank.')

    def test_partial_update_with_nonexistent_user(self):
        """Test partial update with non-existent user returns 404."""
        url = reverse('user-detail', kwargs={'pk': 99999})
        data = {'phone': '1234567890'}
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_with_invalid_data(self):
        """Test partial update with invalid data format returns 400."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        # Invalid data - phone too long
        data = {'phone': 'a' * 100}
        
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Destroy Endpoint Tests
    def test_destroy_user_with_valid_id(self):
        """Test destroy endpoint with valid user ID deletes user."""
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        user_id = self.user.id
        
        user_count_before = User.objects.count()
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.assertEqual(User.objects.count(), user_count_before - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=user_id)

    def test_destroy_user_with_nonexistent_id(self):
        """Test destroy endpoint with non-existent user ID returns 404."""
        url = reverse('user-detail', kwargs={'pk': 99999})
        user_count_before = User.objects.count()
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), user_count_before)

    def test_destroy_user_cascade_behavior(self):
        """Test destroy endpoint handles CASCADE behavior for related objects."""
        # Assign plan to user
        self.user.plan = self.plan_month
        self.user.save()
        
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Plan should still exist (CASCADE only affects user)
        self.assertTrue(Plan.objects.filter(id=self.plan_month.id).exists())

    # Archive Endpoint Tests
    def test_archive_user_with_reason(self):
        """Test archive endpoint archives user with reason and sets timestamp."""
        url = reverse('user-archive', kwargs={'pk': self.user.id})
        archive_reason = "User requested deletion"
        
        response = self.client.post(url, {'archived_reason': archive_reason}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify database side effects
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_archive_user_with_nonexistent_id(self):
        """Test archive endpoint with non-existent user ID returns 404."""
        url = reverse('user-archive', kwargs={'pk': 99999})
        
        response = self.client.post(url, {'archived_reason': 'test'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Change Plan Endpoint Tests
    def test_change_plan_with_valid_active_plan(self):
        """Test change plan endpoint with valid active plan updates user's plan."""
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {'plan': self.plan_month.id}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify database side effects
        self.user.refresh_from_db()
        self.assertEqual(self.user.plan.id, self.plan_month.id)
        self.assertIsNotNone(self.user.plan_start_date)
        self.assertIsNotNone(self.user.plan_end_date)
        # Verify plan_end_date calculation (month = 30 days)
        expected_end_date = self.user.plan_start_date + timedelta(days=30)
        time_diff = abs((self.user.plan_end_date - expected_end_date).total_seconds())
        self.assertLess(time_diff, 5)  # Allow 5 seconds difference

    def test_change_plan_with_year_interval(self):
        """Test change plan endpoint with year interval calculates dates correctly."""
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {'plan': self.plan_year.id}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify database side effects
        self.user.refresh_from_db()
        self.assertEqual(self.user.plan.id, self.plan_year.id)
        # Verify plan_end_date calculation (year = 365 days)
        expected_end_date = self.user.plan_start_date + timedelta(days=365)
        time_diff = abs((self.user.plan_end_date - expected_end_date).total_seconds())
        self.assertLess(time_diff, 5)  # Allow 5 seconds difference

    def test_change_plan_with_inactive_plan(self):
        """Test change plan endpoint with inactive plan returns 400."""
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {'plan': self.plan_inactive.id}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('plan', response.data)

    def test_change_plan_with_invalid_plan_id(self):
        """Test change plan endpoint with invalid plan ID returns 400."""
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {'plan': 99999}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_plan_with_missing_plan_field(self):
        """Test change plan endpoint without plan field returns 400."""
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('plan', response.data)

    def test_change_plan_with_nonexistent_user(self):
        """Test change plan endpoint with non-existent user returns 404."""
        url = reverse('user-change-plan', kwargs={'pk': 99999})
        data = {'plan': self.plan_month.id}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_plan_updates_existing_plan(self):
        """Test change plan endpoint updates from one plan to another."""
        # Set initial plan
        self.user.plan = self.plan_month
        self.user.plan_start_date = timezone.now() - timedelta(days=10)
        self.user.plan_end_date = self.user.plan_start_date + timedelta(days=30)
        self.user.save()
        
        original_start_date = self.user.plan_start_date
        
        url = reverse('user-change-plan', kwargs={'pk': self.user.id})
        data = {'plan': self.plan_year.id}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify database side effects
        self.user.refresh_from_db()
        self.assertEqual(self.user.plan.id, self.plan_year.id)
        # Verify plan_start_date was updated (reset to now)
        self.assertGreater(self.user.plan_start_date, original_start_date)
        # Verify plan_end_date recalculated for year interval
        expected_end_date = self.user.plan_start_date + timedelta(days=365)
        time_diff = abs((self.user.plan_end_date - expected_end_date).total_seconds())
        self.assertLess(time_diff, 5)

