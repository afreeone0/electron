from django.urls import path, include
from . import views
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('carts', views.CartViewSet, basename='carts')
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
    path('v1/', include(router.urls)),

    path('v1/login/', views.LoginAPIView.as_view()),
    path('v1/logout/', views.LogoutAPIView.as_view()),
    path('v1/registration/', views.RegistrationAPIView.as_view()),

    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
