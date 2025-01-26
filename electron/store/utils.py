from .models import Product
from django.db.models import Q


def acceptable(set_query: set):
    for character in '#<>;/\\![]{}()"':
        if character in set_query:
            return False
    return True


def query_search(query):
    if query.isdigit() and len(query) <= 7:
        return Product.objects.filter(id=int(query))
    elif len(query) < 100 and acceptable(set(query)):
        keywords = tuple(filter(lambda word: len(word) > 2, query.split()))
        q_objects = Q()
        for kw in keywords:
            q_objects |= Q(name__icontains=kw) | Q(description__icontains=kw)

        return Product.objects.filter(q_objects)
