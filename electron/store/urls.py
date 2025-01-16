from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('catalog/', views.category, name='catalog'),
]
