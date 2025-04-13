from .models import Order
from django.db.models.signals import pre_save, pre_delete
from utils import get_cache_key
from django.core.cache import cache
from django.dispatch import receiver


@receiver([pre_save, pre_delete], sender=Order)
def handler_order_change(sender, instance, **kwargs):
    cache_key = get_cache_key('orders', 'orders_archive', object_id=instance.user.id)
    cache.delete(cache_key)
