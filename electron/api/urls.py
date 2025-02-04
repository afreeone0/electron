from django.urls import path
from . import views

urlpatterns = [
    path('v1/products/', views.ProductListCreate.as_view()),
    path('v1/products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view()),

    path('v1/categories/', views.CategoryListCreate.as_view()),
    path('v1/categories/<int:pk>/', views.CategoryRetrieve.as_view()),

    path('v1/carts/', views.CartListCreateDestroy.as_view()),
    path('v1/carts/<int:pk>/', views.CartRetrieveUpdateDestroy.as_view()),
]
