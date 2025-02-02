from django.urls import path
from . import views
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='users/password_reset_form.html',
             success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]
