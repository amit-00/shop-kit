import pytest
from django.http import Http404

from apps.identity.models import User
from apps.sellers.models import Seller
from apps.sellers.utils import get_seller, check_seller_owner


@pytest.mark.django_db
class TestGetSeller:
    """Test suite for get_seller utility function."""

    def test_get_seller_with_numeric_id(self):
        """Test get_seller with numeric ID string."""
        user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        seller = Seller.objects.create(
            user=user,
            name="Test Seller",
            slug="test-seller",
            support_email="support@test.com"
        )
        
        result = get_seller(str(seller.id))
        assert result.id == seller.id
        assert result.slug == seller.slug

    def test_get_seller_with_slug(self):
        """Test get_seller with slug string."""
        user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        seller = Seller.objects.create(
            user=user,
            name="Test Seller",
            slug="test-seller",
            support_email="support@test.com"
        )
        
        result = get_seller("test-seller")
        assert result.id == seller.id
        assert result.slug == seller.slug

    def test_get_seller_with_non_existent_id(self):
        """Test get_seller with non-existent ID raises 404."""
        with pytest.raises(Http404):
            get_seller("99999")

    def test_get_seller_with_non_existent_slug(self):
        """Test get_seller with non-existent slug raises 404."""
        with pytest.raises(Http404):
            get_seller("non-existent-slug")

    def test_get_seller_with_invalid_identifier(self):
        """Test get_seller with invalid identifier (not numeric, not valid slug)."""
        # This will try to convert to int, fail, then try slug lookup which will 404
        with pytest.raises(Http404):
            get_seller("invalid-identifier-123")


@pytest.mark.django_db
class TestCheckSellerOwner:
    """Test suite for check_seller_owner utility function."""

    def test_check_seller_owner_with_owner(self):
        """Test check_seller_owner returns True for seller owner."""
        user = User.objects.create_user(
            email="owner@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        seller = Seller.objects.create(
            user=user,
            name="Test Seller",
            slug="test-seller",
            support_email="support@test.com"
        )
        
        assert check_seller_owner(seller, user) is True

    def test_check_seller_owner_with_non_owner(self):
        """Test check_seller_owner returns False for non-owner."""
        owner = User.objects.create_user(
            email="owner@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        non_owner = User.objects.create_user(
            email="nonowner@example.com",
            phone="0987654321",
            first_name="Jane",
            last_name="Smith"
        )
        seller = Seller.objects.create(
            user=owner,
            name="Test Seller",
            slug="test-seller",
            support_email="support@test.com"
        )
        
        assert check_seller_owner(seller, non_owner) is False

    def test_check_seller_owner_with_different_users(self):
        """Test check_seller_owner with multiple different users."""
        user1 = User.objects.create_user(
            email="user1@example.com",
            phone="1111111111",
            first_name="User",
            last_name="One"
        )
        user2 = User.objects.create_user(
            email="user2@example.com",
            phone="2222222222",
            first_name="User",
            last_name="Two"
        )
        seller = Seller.objects.create(
            user=user1,
            name="Test Seller",
            slug="test-seller",
            support_email="support@test.com"
        )
        
        assert check_seller_owner(seller, user1) is True
        assert check_seller_owner(seller, user2) is False

