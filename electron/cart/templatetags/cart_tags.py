from django import template
from ..models import Cart

register = template.Library()


@register.simple_tag()
def user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)

    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(session_key=request.session.session_key).order_by('product__id')
