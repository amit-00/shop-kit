import pytest
from django.http import Http404

from apps.identity.models import User
from apps.shops.models import Shop
from apps.shops.utils import get_shop, check_shop_owner


@pytest.mark.django_db
class TestGetShop:
    """Test suite for get_shop utility function."""

    def test_get_shop_with_numeric_id(self):
        """Test get_shop with numeric ID string."""
        user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        shop = Shop.objects.create(
            user=user,
            name="Test Shop",
            slug="test-shop",
            support_email="support@test.com"
        )
        
        result = get_shop(str(shop.id))
        assert result.id == shop.id
        assert result.slug == shop.slug

    def test_get_shop_with_slug(self):
        """Test get_shop with slug string."""
        user = User.objects.create_user(
            email="test@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        shop = Shop.objects.create(
            user=user,
            name="Test Shop",
            slug="test-shop",
            support_email="support@test.com"
        )
        
        result = get_shop("test-shop")
        assert result.id == shop.id
        assert result.slug == shop.slug

    def test_get_shop_with_non_existent_id(self):
        """Test get_shop with non-existent ID raises 404."""
        with pytest.raises(Http404):
            get_shop("99999")

    def test_get_shop_with_non_existent_slug(self):
        """Test get_shop with non-existent slug raises 404."""
        with pytest.raises(Http404):
            get_shop("non-existent-slug")

    def test_get_shop_with_invalid_identifier(self):
        """Test get_shop with invalid identifier (not numeric, not valid slug)."""
        # This will try to convert to int, fail, then try slug lookup which will 404
        with pytest.raises(Http404):
            get_shop("invalid-identifier-123")


@pytest.mark.django_db
class TestCheckShopOwner:
    """Test suite for check_shop_owner utility function."""

    def test_check_shop_owner_with_owner(self):
        """Test check_shop_owner returns True for shop owner."""
        user = User.objects.create_user(
            email="owner@example.com",
            phone="1234567890",
            first_name="John",
            last_name="Doe"
        )
        shop = Shop.objects.create(
            user=user,
            name="Test Shop",
            slug="test-shop",
            support_email="support@test.com"
        )
        
        assert check_shop_owner(shop, user) is True

    def test_check_shop_owner_with_non_owner(self):
        """Test check_shop_owner returns False for non-owner."""
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
        shop = Shop.objects.create(
            user=owner,
            name="Test Shop",
            slug="test-shop",
            support_email="support@test.com"
        )
        
        assert check_shop_owner(shop, non_owner) is False

    def test_check_shop_owner_with_different_users(self):
        """Test check_shop_owner with multiple different users."""
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
        shop = Shop.objects.create(
            user=user1,
            name="Test Shop",
            slug="test-shop",
            support_email="support@test.com"
        )
        
        assert check_shop_owner(shop, user1) is True
        assert check_shop_owner(shop, user2) is False

