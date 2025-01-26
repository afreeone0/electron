from .models import Product
from django.contrib.postgres.search import SearchVector


def acceptable(set_query: set):
    for character in '#<>;/\\![]{}()"':
        if character in set_query:
            return False
    return True


def query_search(query):
    if query.isdigit() and len(query) <= 7:
        return Product.objects.filter(id=int(query))
    elif len(query) < 100 and acceptable(set(query)):
        return Product.objects.annotate(search=SearchVector('name', 'description')).filter(search=query)
