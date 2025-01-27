from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Category, Product
from django.core.paginator import Paginator
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
    products = Product.objects.filter(category=category_object, quantity__gte=1)
    if query:
        products = query_search(query, products)

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
