from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

from apps.identity.domain.utils import get_plan_duration

from ..common.model_utils import TimestampedModel, Currency


class Plan(models.Model):
    class Interval(models.Choices):
        MONTH = "month"
        YEAR = "year"

    code = models.CharField(max_length=20, unique=True)
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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password=None, **extra_fields)

    def update_subscription(self, user_id: str, plan: 'Plan') -> 'User':
        duration = get_plan_duration(plan.interval)
        
        user = self.get(pk=user_id)

        user.plan = plan
        user.plan_start_date = timezone.now()
        user.plan_end_date = user.plan_start_date + duration
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimestampedModel):
    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe'
        CARD = 'card'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True) #City/Town
    administrative_area = models.CharField(max_length=255, null=True, blank=True) #State/Province
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    plan_start_date = models.DateTimeField(null=True, blank=True)
    plan_end_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CARD)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def set_password(self, password):
        super().set_unusable_password()
    
    def check_password(self, password):
        return False

    def has_usable_password(self):
        return False

    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['email']),
        ]
