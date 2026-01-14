from django.db import models

from apps.common.model_utils import TimestampedModel, Currency
from apps.sellers.models import Seller, Product, Price
from apps.identity.models import User

class Order(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        SHIPPED = 'shipped'
        DELIVERED = 'delivered'
        CANCELLED = 'cancelled'

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        indexes = [
            models.Index(fields=['seller']),
            models.Index(fields=['user']),
        ]

class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    unit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)