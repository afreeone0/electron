from .models import User
from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import pre_save, pre_delete
from utils import get_cache_key


@receiver([pre_save, pre_delete], sender=User)
def handler_user_change(sender, instance, **kwargs):
    profile_cache_key = get_cache_key('users', 'profile', instance.id)
    orders_cache_key = get_cache_key('orders', 'orders_archive', instance.id)
    cache.delete_many([profile_cache_key, orders_cache_key])
