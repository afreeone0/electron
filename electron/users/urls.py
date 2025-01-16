from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.register, name='registration'),
    path('profile/', views.profile, name='profile'),
]
