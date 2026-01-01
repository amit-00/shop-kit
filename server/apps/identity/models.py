from django.db import models
from django.conf import settings

from ..common.model_utils import TimestampedModel


class Plan(models.Model):
    class Currency(models.choices):
        USD = "usd"
        CAD = "cad"

    class Interval(models.choices):
        MONTH = "month"
        YEAR = "year"

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_amount = models.IntegerField()
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    interval = models.CharField(max_length=255, choices=Interval.choices, default=Interval.MONTH)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.code

    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]


class User(TimestampedModel):
    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe'
        CARD = 'card'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    plan_start_date = models.DateTimeField(null=True, blank=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_reason = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'is_archived']),
            models.Index(fields=['email', 'is_archived']),
        ]
