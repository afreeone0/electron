from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('v1/', include(router.urls)),

    path('v1/carts/', views.CartListCreateDestroy.as_view()),
    path('v1/carts/<int:pk>/', views.CartRetrieveUpdateDestroy.as_view()),

]
