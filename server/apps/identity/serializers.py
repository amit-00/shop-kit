from rest_framework import serializers
from .models import User, Plan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'is_active']


class ChangePlanSerializer(serializers.Serializer):
    plan_code = serializers.CharField(required=True)
    payment_method = serializers.ChoiceField(required=True, choices=User.PaymentMethod.choices)

    def validate_plan_code(self, value: str) -> str:
        try:
            plan = Plan.objects.get(code=value, is_active=True)
        except Plan.DoesNotExist:
            raise serializers.ValidationError('Invalid plan code')
        
        self.instance = plan
        return value

    def validate(self, attrs: dict) -> dict:
        plan = self.instance
        if plan.interval not in [Plan.Interval.MONTH, Plan.Interval.YEAR]:
            raise serializers.ValidationError('Invalid plan interval')
        return attrs
