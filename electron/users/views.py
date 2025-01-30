from django.shortcuts import render, redirect, reverse
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, 'Logged in successfully!')

                if session_key:
                    # Cart.objects.filter(session_key=session_key).update(user=user)
                    for cart_not_auth in Cart.objects.filter(session_key=session_key):
                        cart_auth = Cart.objects.filter(user=user, product=cart_not_auth.product)[0]
                        if cart_auth:
                            cart_auth.quantity += cart_not_auth.quantity
                            cart_auth.save()
                        else:
                            cart_not_auth.user = user
                            cart_not_auth.save()

                return redirect(reverse('index'), permanent=True)
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
            session_key = request.session.session_key

            form.save()
            messages.success(request, 'Registered successfully!')
            auth.login(request, form.instance)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=form.instance)

            return redirect(reverse('index'), permanent=True)
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
