from django.urls import path
from . import views

urlpatterns = [
    path('v1/products/', views.ProductsAPIView.as_view()),
]
