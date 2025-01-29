from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('cart/add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart/take_away/<slug:product_slug>/', views.cart_take_away, name='cart_take_away'),
    path('cart/remove/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
    path('cart/clear_up/', views.cart_clear_up, name='cart_clear_up'),
]
