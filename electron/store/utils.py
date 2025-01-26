from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def acceptable(set_query: set):
    for character in '#<>;/\\![]{}()"':
        if character in set_query:
            return False
    return True


def query_search(query):
    if query.isdigit() and len(query) <= 7:
        return Product.objects.filter(id=int(query))
    elif len(query) < 100 and acceptable(set(query)):
        vector = SearchVector('name', 'description')
        query = SearchQuery(query)
        return Product.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
