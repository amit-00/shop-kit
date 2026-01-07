from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PlanViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='user')
router.register(r'plans', PlanViewSet, basename='plan')

urlpatterns = router.urls