from django.urls import path
from .views import PriceViewSet, ProductViewSet, ShopViewSet

urlpatterns = [
    # Shop endpoints
    path('', ShopViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='shop-list'),
    path('<str:identifier>', ShopViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='shop-detail'),
    
    # Product endpoints (nested under shop)
    path('<str:identifier>/products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='product-list'),
    path('<str:identifier>/products/<str:product_id>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='product-detail'),
    
    # Price endpoints (nested under shop and product)
    path('<str:identifier>/products/<str:product_id>/prices', PriceViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='price-list'),
    path('<str:identifier>/products/<str:product_id>/prices/<str:price_id>', PriceViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='price-detail'),
]

