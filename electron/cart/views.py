from django.shortcuts import render, redirect, get_object_or_404
from .mixins import CartMixin
from .models import Cart
from store.models import Product
from django.views.generic import TemplateView, View


class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Моя корзина'
        return context


class CartAddView(CartMixin, View):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, product_slug=product_slug)
        user_cart = self.get_cart(request, product=product)
        if user_cart:
            user_cart.quantity += 1
            user_cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)

        return redirect(request.META['HTTP_REFERER'])


class CartTakeAwayView(CartMixin, View):
    def get(self, request, product_slug):
        product = Product.objects.get(product_slug=product_slug)
        user_cart = self.get_cart(request, product=product)
        if user_cart:
            if user_cart.quantity >= 2:
                user_cart.quantity -= 1
                user_cart.save()
            else:
                user_cart.delete()

        return redirect(request.META['HTTP_REFERER'])


class CartClearUpView(CartMixin, View):
    def get(self, request):
        user_carts = self.get_cart(request)
        if user_carts.exists():
            for user_cart in user_carts:
                user_cart.delete()

        return redirect(request.META['HTTP_REFERER'])


class CartRemoveView(CartMixin, View):
    def get(self, request, product_slug):
        product = Product.objects.get(product_slug=product_slug)
        user_cart = self.get_cart(request, product)
        user_cart.delete()
        return redirect(request.META['HTTP_REFERER'])
