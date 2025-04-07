from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Category, Product
from .utils import query_search
from django.views.generic import TemplateView, DetailView, ListView
from django.core.cache import cache
import logging

logger = logging.getLogger('store_logger')


class IndexView(TemplateView):
    template_name = 'store/index.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'user {request.user} sent a get request for the index page')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Electron'
        return context


def page_not_found(request, exception=None):
    template404 = render_to_string('page_not_found.html')
    return HttpResponseNotFound(template404)


class AboutView(TemplateView):
    template_name = 'store/about.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'user {request.user} sent a get request for the about page')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        return context


class CategoryView(ListView):
    model = Product
    template_name = 'store/category.html'
    context_object_name = 'products'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        logger.info(f'user {request.user} requests a category page ({request.path})')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        logger.debug('forming a queryset for the request')
        category_slug = self.kwargs.get('category_slug')
        query_params = {
            'discount': self.request.GET.get('discount'),
            'order_by_price': self.request.GET.get('order_by_price'),
            'query': self.request.GET.get('q'),
        }
        logger.debug(f'query params of the request: {query_params}')

        cache_params = {k: v for k, v in query_params.items() if v is not None}
        cache_key = f'category:{category_slug}' + '&'.join(cache_params)
        products = cache.get(cache_key)

        if products is None:
            category_object = get_object_or_404(Category, category_slug=category_slug)
            self.kwargs['category_object'] = category_object

            products = super().get_queryset().filter(category=category_object, quantity__gte=1)
            logger.debug('got the products queryset')
            if query_params['query']:
                products = query_search(query_params['query'], products)

            if query_params['discount']:
                products = products.filter(discount__gt=0)

            if query_params['order_by_price'] and query_params['order_by_price'] != 'default':
                products = products.order_by(query_params['order_by_price'])

            cache.set(cache_key, products.values())
        logger.debug('returning the queryset')
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category_slug'] = self.kwargs.get('category_slug')
        context['title'] = self.kwargs.get('category_object').name
        return context


class ProductView(DetailView):
    template_name = 'store/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get(self, request, *args, **kwargs):
        logger.info(f'user {request.user} requests for the product page ({request.path})')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        product_slug = self.kwargs.get(self.slug_url_kwarg)
        cache_key = f'product_slug:{product_slug}'
        product_object = cache.get(cache_key)
        if product_object is None:
            product_object = (get_object_or_404(Product, product_slug=product_slug),)
            cache.set(cache_key, product_object)
        logger.debug('returning the object user requested a detailed view for')
        return product_object[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
