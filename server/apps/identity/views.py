from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import User, Subscription
from .serializers import UserSerializer, SubscriptionSerializer

class UserViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def list(self, request: Request) -> Response:
        email = request.query_params.get('email')
        
        if not email:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error': 'Email is required'}
            )

        users = self.queryset.filter(email=email)

        if not users.exists():
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'error': 'User not found'}
            )

        serializer = self.serializer_class(users.first())
        return Response(serializer.data)


    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                Subscription.objects.create(
                    user=serializer.instance,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timedelta(days=365),
                    tier=Subscription.Tier.FREE
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


    def update(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)