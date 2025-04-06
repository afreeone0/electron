from django.shortcuts import redirect
from django.template.loader import render_to_string

from .mixins import CartMixin
from .models import Cart
from store.models import Product
from django.views.generic import TemplateView, View
from django.http import JsonResponse
import logging

format__ = "%(asctime)s %(levelname)s %(message)s"
logger = logging.getLogger('electron.cart_views')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename='cart_views.log')
formatter_ = logging.Formatter(fmt=format__)
file_handler.setFormatter(formatter_)
logger.addHandler(file_handler)


class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Моя корзина'
        return context


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        logger.debug(f'product_id: {product_id}')
        user_cart = self.get_cart(request, product=product_id)
        logger.debug(f'got a cart: {user_cart}')
        if user_cart:
            user_cart.quantity += 1
            user_cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product_id=product_id, quantity=1)
        return JsonResponse({'status': 200})


class CartTakeAwayView(CartMixin, View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        user_cart = self.get_cart(request, product=product_id)
        if user_cart:
            if user_cart.quantity >= 2:
                user_cart.quantity -= 1
                user_cart.save()
            else:
                user_cart.delete()

        return JsonResponse({'status': 200})


class CartClearUpView(CartMixin, View):
    def post(self, request):
        user_carts = self.get_cart(request)
        if user_carts.exists():
            for user_cart in user_carts:
                user_cart.delete()

        return JsonResponse({'status': 204})


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        user_cart = self.get_cart(request, cart_id=cart_id)
        user_cart.delete()
        return JsonResponse({'status': 204})
