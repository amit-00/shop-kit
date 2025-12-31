from django.db import models
from common.model_utils import TimestampedModel


class User(TimestampedModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

class Subscription(TimestampedModel):
    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe'
        CARD = 'card'

    class Tier(models.TextChoices):
        FREE = 'free'
        PREMIUM = 'premium'
        CUSTOM = 'custom'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    tier = models.CharField(max_length=255, choices=Tier.choices, default=Tier.FREE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cancel_date = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['tier']),
            models.Index(fields=['start_date'])
        ]