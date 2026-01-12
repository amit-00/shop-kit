from typing import Optional
from django.core.cache import cache


def get_redis_client():
    """Returns Redis connection using django-redis cache."""
    return cache


def get_jti_key(jti: str) -> str:
    return f"magic_link:jti:{jti}"


def store_magic_link_jti(jti: str, user_id: str, ttl_seconds: int) -> None:
    """
    Stores JTI in Redis with TTL.
    """
    key = get_jti_key(jti)
    cache.set(key, user_id, timeout=ttl_seconds)


def get_magic_link_jti(jti: str) -> Optional[str]:
    """
    Retrieves user_id from Redis by JTI.
    """
    key = get_jti_key(jti)
    return cache.get(key)


def delete_magic_link_jti(jti: str) -> None:
    """
    Deletes JTI from Redis (for single-use tokens).
    """
    key = get_jti_key(jti)
    cache.delete(key)

