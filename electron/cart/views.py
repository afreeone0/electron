from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from store.models import Product


def cart(request):
    context = {
        'title': 'Your cart',
    }
    return render(request, 'cart/cart.html', context=context)


def cart_add(request, product_slug):
    product = Product.objects.get(product_slug=product_slug)
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user, product=product)
        if not user_carts.exists():
            Cart.objects.create(user=request.user, product=product, quantity=1)
        else:
            user_cart = user_carts[0]
            user_cart.quantity += 1
            user_cart.save()
    else:
        user_carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if not user_carts.exists():
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
        else:
            user_cart = user_carts[0]
            user_cart.quantity += 1
            user_cart.save()
    return redirect(request.META['HTTP_REFERER'])


def cart_take_away(request, product_slug):
    product = Product.objects.get(product_slug=product_slug)
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user, product=product)
        if user_carts.exists():
            user_cart = user_carts[0]
            if user_cart.quantity >= 2:
                user_cart.quantity -= 1
                user_cart.save()
            else:
                user_cart.delete()
    else:
        user_carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if user_carts.exists():
            user_cart = user_carts[0]
            if user_cart.quantity >= 2:
                user_cart.quantity -= 1
                user_cart.save()
            else:
                user_cart.delete()
    return redirect(request.META['HTTP_REFERER'])


def cart_clear_up(request):
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user)
        if user_carts.exists():
            for user_cart in user_carts:
                user_cart.delete()
    else:
        user_carts = Cart.objects.filter(session_key=request.session.session_key)
        if user_carts.exists():
            for user_cart in user_carts:
                user_cart.delete()

    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, product_slug):
    product = Product.objects.get(product_slug=product_slug)
    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user, product=product)
        if user_carts.exists():
            user_cart = user_carts[0]
            user_cart.delete()
    else:
        user_carts = Cart.objects.filter(session_key=request.session.session_key, product=product)
        if user_carts.exists():
            user_cart = user_carts[0]
            user_cart.delete()
    return redirect(request.META['HTTP_REFERER'])
