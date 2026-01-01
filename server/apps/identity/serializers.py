from datetime import timedelta

from rest_framework import serializers
from django.utils import timezone
from .models import User, Plan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'phone', 
            'first_name', 
            'last_name',
            'plan',
            'plan_start_date',
            'plan_end_date',
        ]

    def create(self, validated_data: dict) -> User:
        plan = Plan.objects.get(
            code='free',
            is_active=True
        )

        if not plan:
            raise serializers.ValidationError('Free plan is not available')
        
        user = User.objects.create(
            **validated_data,
            plan=plan
        )
        user.plan_start_date = timezone.now()
        user.save()
        return user
        

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
        duration = 30 if plan.interval == Plan.Interval.MONTH else 365
        
        instance.plan = plan
        instance.plan_start_date = timezone.now()
        instance.plan_end_date = timezone.now() + timedelta(days=duration)
        instance.save()
        return instance