from .mixins import CartMixin
from .models import Cart
from django.views.generic import TemplateView, View
from django.http import JsonResponse
import logging
from django.views.decorators.cache import cache_page

logger = logging.getLogger('cart_logger')


class CartView(TemplateView):
    template_name = 'cart/cart.html'

    def get(self, request, *args, **kwargs):
        logger.info(f'user {request.user} requested the cart page')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Моя корзина'
        return context


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        logger.info(f'user: {request.user}, POST request to add a product to the cart, product_id: {product_id}')
        user_cart = self.get_cart(request, product=product_id)
        logger.debug(f'user cart is: {user_cart}')
        if user_cart:
            user_cart.quantity += 1
            user_cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product_id=product_id, quantity=1)
        logger.debug('ready to return 200 response status')
        return JsonResponse({'status': 200})


class CartTakeAwayView(CartMixin, View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        logger.info(f'user: {request.user}, POST request to take away one product from the cart, product_id: {product_id}')
        user_cart = self.get_cart(request, product=product_id)
        logger.debug(f'user cart is: {user_cart}')
        if user_cart:
            if user_cart.quantity >= 2:
                user_cart.quantity -= 1
                user_cart.save()
            else:
                user_cart.delete()
        logger.debug('ready to return 200 response status')
        return JsonResponse({'status': 200})


class CartClearUpView(CartMixin, View):
    def post(self, request):
        logger.info(f'user: {request.user}, received a POST-request to clear up the cart')
        user_carts = self.get_cart(request)
        if user_carts.exists():
            for user_cart in user_carts:
                user_cart.delete()
        logger.debug('ready to return 204 response status')
        return JsonResponse({'status': 204})


class CartRemoveView(CartMixin, View):
    def post(self, request):
        logger.info(f'user: {request.user}, received a POST-request to remove a product from the cart')
        cart_id = request.POST.get('cart_id')
        user_cart = self.get_cart(request, cart_id=cart_id)
        user_cart.delete()
        logger.debug('ready to return 204 response status')
        return JsonResponse({'status': 204})
