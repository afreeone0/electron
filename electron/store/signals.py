from .models import Category, Product
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.cache.utils import make_template_fragment_key
from django.core.cache import cache
from utils import get_cache_key


@receiver([pre_save, pre_delete], sender=Product)
def handler_product_change(sender, instance, **kwargs):
    navbar_catalog_cache_key = make_template_fragment_key("navbar_catalog")
    product_url_kwargs = {'product_slug': instance.product_slug}
    product_cache_key = get_cache_key('store', 'product', url_kwargs=product_url_kwargs)
    category_url_kwargs = {'category_slug': instance.category.category_slug}
    category_cache_key = get_cache_key('store', 'category', url_kwargs=category_url_kwargs)
    cache.delete_many([
        navbar_catalog_cache_key,
        product_cache_key,
        category_cache_key
    ])


@receiver([pre_save, pre_delete], sender=Category)
def handler_category_change(sender, instance, **kwargs):
    navbar_catalog_cache_key = make_template_fragment_key("navbar_catalog")
    url_kwargs = {'category_slug': instance.category_slug}
    category_cache_key = get_cache_key('store', 'category', url_kwargs=url_kwargs)
    cache.delete_many([navbar_catalog_cache_key, category_cache_key])
