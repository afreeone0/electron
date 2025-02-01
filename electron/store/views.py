from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Category, Product
from .utils import query_search
from django.views.generic import TemplateView, DetailView, ListView


class IndexView(TemplateView):
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Electron'
        return context


def page_not_found(request, exception=None):
    template404 = render_to_string('page_not_found.html')
    return HttpResponseNotFound(template404)


class AboutView(TemplateView):
    template_name = 'store/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        return context


class CategoryView(ListView):
    model = Product
    queryset = Product.objects.order_by('-id')
    template_name = 'store/category.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        discount = self.request.GET.get('discount')
        order_by_price = self.request.GET.get('order_by_price')
        query = self.request.GET.get('q')

        category_object = get_object_or_404(Category, category_slug=category_slug)
        self.kwargs['category_object'] = category_object

        products = super().get_queryset().filter(category=category_object, quantity__gte=1)
        if query:
            products = query_search(query, products)

        if discount:
            products = products.filter(discount__gt=0)

        if order_by_price and order_by_price != 'default':
            products = products.order_by(order_by_price)

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

    def get_object(self, queryset=None):
        product_object = get_object_or_404(Product, product_slug=self.kwargs.get(self.slug_url_kwarg))
        return product_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
