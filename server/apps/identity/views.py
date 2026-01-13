from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from apps.identity.domain.utils import format_validation_errors

from .models import User, Plan
from .serializers import *


class UserViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override to allow public access for list and create actions.
        """
        if self.action in ['list', 'create']:
            return [AllowAny()]
        return [IsAuthenticated()]

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
            formatted_errors = format_validation_errors(serializer.errors)
            return Response({ 'errors': formatted_errors }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk: str) -> Response:
        # Validate the pk parameter using serializer
        input_serializer = RetrieveUserSerializer(data={'pk': pk})
        
        if not input_serializer.is_valid():
            formatted_errors = format_validation_errors(input_serializer.errors)
            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
        
        validated_pk = input_serializer.validated_data['pk']
        user = get_object_or_404(self.queryset, id=validated_pk)

        serializer = UserRetrieveSerializer(user)
        return Response(serializer.data)
    
    def partial_update(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        
        # Map phone_number from request to phone for serializer
        update_data = {}
        if 'phone' in request.data:
            update_data['phone'] = request.data['phone'] 
        if 'first_name' in request.data:
            update_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data:
            update_data['last_name'] = request.data['last_name']

        serializer = self.serializer_class(
            user, 
            data=update_data, 
            partial=True
        )

        if not serializer.is_valid():
            formatted_errors = format_validation_errors(serializer.errors)
            print(formatted_errors)
            return Response({ 'errors': formatted_errors }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)
        user.is_active = False
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
    permission_classes = [IsAuthenticated]