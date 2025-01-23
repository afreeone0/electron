from django import template
from django.utils.http import urlencode
from ..models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.order_by('name')


@register.simple_tag(takes_context=True)
def add_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
