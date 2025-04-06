from cart.models import Cart


class CartMixin:
    def get_cart(self, request, product=None, cart_id=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}

        if product:
            query_kwargs['product'] = product
            return Cart.objects.filter(**query_kwargs).first()

        if cart_id:
            query_kwargs['pk'] = cart_id

        return Cart.objects.filter(**query_kwargs)
