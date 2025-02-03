# from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline


def acceptable(set_query: set):
    for character in '#<>;/\\![]{}()"':
        if character in set_query:
            return False
    return True


def query_search(query, products, api=False):
    if query.isdigit() and len(query) <= 7:
        return products.filter(id=int(query))
    elif len(query) < 100 and acceptable(set(query)):
        vector = SearchVector('name', 'description')
        query = SearchQuery(query)
        result = products.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by('-rank')
        if api:
            return result
        result = result.annotate(headline=SearchHeadline(
            'name',
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>'))
        return result.annotate(bodyline=SearchHeadline(
            'description',
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>'))
    else:
        return products
