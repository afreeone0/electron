from cart.models import Cart


class CartMixin:
    def get_cart(self, request, product=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}

        if product:
            query_kwargs['product'] = product
            return Cart.objects.filter(**query_kwargs).first()

        return Cart.objects.filter(**query_kwargs)
