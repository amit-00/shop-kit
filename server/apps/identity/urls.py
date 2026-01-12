from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PlanViewSet
from .auth_views import LoginRequestView, RegisterRequestView, MagicLinkVerifyView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'plans', PlanViewSet, basename='plan')

urlpatterns = [
    path('auth/register', RegisterRequestView.as_view(), name='auth-register'),
    path('auth/login', LoginRequestView.as_view(), name='auth-login'),
    path('auth/verify', MagicLinkVerifyView.as_view(), name='auth-verify'),
] + router.urls