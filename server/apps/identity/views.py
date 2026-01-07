from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import User, Plan
from .serializers import *

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

        user = get_object_or_404(self.queryset, email=email)
        serializer = UserRetrieveSerializer(user)
        return Response(serializer.data)


    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)

        serializer = UserRetrieveSerializer(user)
        return Response(serializer.data)

    
    def partial_update(self, request: Request, pk: str) -> Response:
        phone = request.data.get('phone_number')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        user = get_object_or_404(self.queryset, id=pk)
        serializer = self.serializer_class(
            user, 
            data={'phone': phone, 'first_name': first_name, 'last_name': last_name}, 
            partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def destroy(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        user.is_archived = True
        user.archived_at = timezone.now()
        user.archived_reason = request.data.get('archived_reason')
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=True, methods=['patch'], url_path='change-plan')
    def change_plan(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        serializer = ChangePlanSerializer(instance=user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = []