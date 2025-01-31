from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
