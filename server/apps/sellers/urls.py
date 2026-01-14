from django.urls import path
from .views import PriceViewSet, ProductViewSet, SellerViewSet

urlpatterns = [
    # Seller endpoints
    path('', SellerViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='seller-list'),
    path('<str:identifier>', SellerViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='seller-detail'),
    
    # Product endpoints (nested under seller)
    path('<str:identifier>/products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='product-list'),
    path('<str:identifier>/products/<str:product_id>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='product-detail'),
    
    # Price endpoints (nested under seller and product)
    path('<str:identifier>/products/<str:product_id>/prices', PriceViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='price-list'),
    path('<str:identifier>/products/<str:product_id>/prices/<str:price_id>', PriceViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='price-detail'),
]

