from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from .models import User, Plan
from .serializers import UserSerializer, ChangePlanSerializer

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
        serializer = self.serializer_class(user)
        return Response(serializer.data)


    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan = Plan.objects.get(code='free', is_active=True)
        if not plan:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'error': 'Free plan is not available'}
            )

        user = serializer.save(plan=plan)
        user.plan_start_date = timezone.now()
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request: Request, pk: str) -> Response:
        user = get_object_or_404(self.queryset, id=pk)

        serializer = self.serializer_class(user)
        return Response(serializer.data)

    
    def partial_update(self, request: Request, pk: str) -> Response:
        phone, first_name, last_name = request.data

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
        return Response(status=status.HTTP_204_OK)


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
        serializer = ChangePlanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan = serializer.instance
        duration = 30 if plan.interval == Plan.Interval.MONTH else 365

        user = get_object_or_404(self.queryset, id=pk)
        user.plan = plan
        user.plan_start_date = timezone.now()
        user.plan_end_date = user.plan_start_date + timedelta(days=duration)
        user.payment_method = serializer.validated_data.get('payment_method')
        user.save()
        return Response(status=status.HTTP_204_OK)
