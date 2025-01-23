from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('cart/add/<int:product_id>/', views.add_to_the_cart, name='cart_add'),
    path('cart/take_away/<int:product_id>/', views.take_one_away, name='take_away'),
    path('cart/clear_up/', views.clear_up_the_cart, name='clear_up'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove'),
]

