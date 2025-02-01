from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
