from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('take_away/<slug:product_slug>/', views.cart_take_away, name='cart_take_away'),
    path('remove/<slug:product_slug>/', views.cart_remove, name='cart_remove'),
    path('clear_up/', views.cart_clear_up, name='cart_clear_up'),
]
