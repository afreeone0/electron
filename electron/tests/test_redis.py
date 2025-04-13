from django.core.cache import cache as redis_cache
from time import sleep
from django.urls import reverse
from django.core.cache.utils import make_template_fragment_key
import pytest


def test_redis_basic_availability():
    redis_cache.set('k1', 'v1', -1)
    assert redis_cache.get('k1') == 'v1'
    assert redis_cache.delete('k1')
    redis_cache.set('k2', 'v2', 1)
    sleep(1.2)
    assert redis_cache.get('k2') == 'v2'
    redis_cache.set_many({'k3': 'v3', 'k4': 'v4'})
    assert redis_cache.delete_many(['k2', 'k3', 'k4'])
    redis_cache.set('k5', 'v5')
    redis_cache.clear()
    assert not redis_cache.get('k5')


@pytest.mark.django_db
def test_redis_page_caching(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    catalog_cache_key = make_template_fragment_key("navbar_catalog")
    assert redis_cache.get(catalog_cache_key)
    redis_cache.clear()
