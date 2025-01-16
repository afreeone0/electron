from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import User
from django import forms


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={}))

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={}))
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))

    class Meta:
        model = User
        fields = ('nickname', 'username', 'email')
