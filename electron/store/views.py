from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string


def index(request):
    context = {
        'title': 'Electron',
    }
    return render(request, 'store/index.html', context=context)


def page_not_found(request, exception):
    template404 = render_to_string('page_not_found.html')
    return HttpResponseNotFound(template404)


def about(request):
    context = {
        'title': 'About us',
    }
    return render(request, 'store/about.html', context=context)


def category(request, category_slug=None):
    context = {
        'title': 'Catalog',
    }
    return render(request, 'store/category.html', context=context)


def cart(request):
    context = {
        'title': 'Your cart',
    }
    return render(request, 'store/cart.html', context=context)
