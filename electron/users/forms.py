from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .models import User
from django import forms
from validators import get_validators_list


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={}))
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))

    def clean_image(self):
        image = self.cleaned_data['image']
        for validator in get_validators_list():
            validator(image)
        return image

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')
