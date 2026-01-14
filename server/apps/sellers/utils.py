from django.shortcuts import get_object_or_404

from .models import Seller


def get_seller(identifier: str) -> Seller:
    """
    Auto-detect identifier type: try ID first, then slug.
    """
    seller_queryset = Seller.objects.all()
    try:
        seller_id = int(identifier)
        return get_object_or_404(seller_queryset, id=seller_id)
    except (ValueError, TypeError):
        # Fall back to slug lookup
        return get_object_or_404(seller_queryset, slug=identifier)


def check_seller_owner(seller: Seller, user) -> bool:
    """
    Check if user owns the seller.
    """
    return seller.user == user

