from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from django.contrib import auth, messages


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.username
            password = form.password
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                url = reverse('index')
                redirect(url, permanent=True)
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context=context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse('profile')
            return redirect(url, permanent=True)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
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
    }
    return render(request, 'users/registration.html', context=context)
