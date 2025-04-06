from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('add/', views.CartAddView.as_view(), name='cart_add'),
    path('take_away/', views.CartTakeAwayView.as_view(), name='cart_take_away'),
    path('remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('clear_up/', views.CartClearUpView.as_view(), name='cart_clear_up'),
]
