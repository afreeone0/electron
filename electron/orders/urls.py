from django.urls import path
from . import views

urlpatterns = [
    path('make_order/', views.MakeOrderView.as_view(), name='make_order'),
    path('orders_archive/', views.OrdersArchiveView.as_view(), name='orders_archive'),
]
