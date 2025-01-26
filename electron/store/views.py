from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Category, Product, Cart
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .utils import query_search


def index(request):
    context = {
        'title': 'Electron',
    }
    return render(request, 'store/index.html', context=context)


def page_not_found(request, exception=None):
    template404 = render_to_string('page_not_found.html')
    return HttpResponseNotFound(template404)


def about(request):
    context = {
        'title': 'About us',
    }
    return render(request, 'store/about.html', context=context)


def category(request, category_slug):
    page = int(request.GET.get('page', 1))

    discount = request.GET.get('discount', None)
    order_by_price = request.GET.get('order_by_price', None)
    query = request.GET.get('q', None)

    category_object = get_object_or_404(Category, category_slug=category_slug)
    products = Product.objects.filter(category=category_object)
    if query:
        products = query_search(query)

    if discount:
        products = products.filter(discount__gt=0)

    if order_by_price and order_by_price != 'default':
        products = products.order_by(order_by_price)

    paginated_products = Paginator(products, 15)
    products_on_page = paginated_products.page(page)
    context = {
        'title': category_object.name,
        'products': products_on_page,
        'selected_category_slug': category_slug,
    }
    return render(request, 'store/category.html', context=context)


@login_required(login_url='login')
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    context = {
        'title': 'Your cart',
        'carts': carts,
    }
    return render(request, 'store/cart.html', context=context)


@login_required(login_url='login')
def add_to_the_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_carts = Cart.objects.filter(user=request.user, product=product)
    if not user_carts.exists():
        Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        user_cart = user_carts[0]
        user_cart.quantity += 1
        user_cart.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def take_one_away(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_carts = Cart.objects.filter(user=request.user, product=product)
    if user_carts.exists():
        user_cart = user_carts[0]
        if user_cart.quantity >= 2:
            user_cart.quantity -= 1
            user_cart.save()
        else:
            user_cart.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def clear_up_the_cart(request):
    user_carts = Cart.objects.filter(user=request.user)
    if user_carts.exists():
        for user_cart in user_carts:
            user_cart.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_carts = Cart.objects.filter(user=request.user, product=product)
    if user_carts.exists():
        user_cart = user_carts[0]
        user_cart.delete()
    return redirect(request.META['HTTP_REFERER'])
