from django.db import models

from apps.common.model_utils import TimestampedModel
from apps.sellers.models import Seller
from apps.identity.models import User

class Order(TimestampedModel):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id