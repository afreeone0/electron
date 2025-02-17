from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('carts', views.CartViewSet, basename='carts')

urlpatterns = [
    path('v1/', include(router.urls)),

    path('v1/login/', views.LoginAPIView.as_view()),
]
