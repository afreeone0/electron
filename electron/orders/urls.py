from django.urls import path
from . import views

urlpatterns = [
    path('make_order/', views.make_order, name='make_order'),
    path('orders_archive/', views.orders_archive, name='orders_archive'),
]
