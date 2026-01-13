from django.shortcuts import get_object_or_404

from .models import Shop


def get_shop(identifier: str) -> Shop:
    """
    Auto-detect identifier type: try ID first, then slug.
    """
    shop_queryset = Shop.objects.all()
    try:
        shop_id = int(identifier)
        return get_object_or_404(shop_queryset, id=shop_id)
    except (ValueError, TypeError):
        # Fall back to slug lookup
        return get_object_or_404(shop_queryset, slug=identifier)


def check_shop_owner(shop: Shop, user) -> bool:
    """
    Check if user owns the shop.
    """
    return shop.user == user

