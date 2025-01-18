from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                url = reverse('index')
                return redirect(url, permanent=True)
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Login',
    }
    return render(request, 'users/login.html', context=context)


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            url = reverse('profile')
            return redirect(url, permanent=True)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'title': 'Profile',
    }
    return render(request, 'users/profile.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered successfully!')
            url = reverse('login')
            return redirect(url, permanent=True)
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Registration',
    }
    return render(request, 'users/registration.html', context=context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    url = reverse('index')
    return redirect(url)
