from rest_framework import serializers
from .models import User, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'is_active']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'stripe_subscription_id', 'stripe_price_id', 'payment_method', 'tier', 'start_date', 'end_date', 'cancel_date', 'cancel_reason']