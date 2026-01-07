from datetime import timedelta

from rest_framework import serializers
from django.utils import timezone
from .models import User, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'code', 'name', 'description', 'unit_amount', 'currency', 'interval', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'phone', 
            'first_name', 
            'last_name',
        ]

    def create(self, validated_data: dict) -> User:
        user = User.objects.create(
            **validated_data
        )
        user.save()
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'phone', 
            'first_name', 
            'last_name',
            'country',
            'line1',
            'line2',
            'locality',
            'administrative_area',
            'postal_code',
            'plan',
            'plan_start_date',
            'plan_end_date',
            'payment_method',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = '__all__'


class RegisterationSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['country_code', 'payment_method']
    

class ChangePlanSerializer(serializers.Serializer):
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True), 
        required=True
    )

    class Meta:
        model = User
        fields = ['plan']

    def update(self, instance: User, validated_data: dict) -> User:
        plan = validated_data.get('plan')
        return User.objects.update_subscription(instance.pk, plan)
