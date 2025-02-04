import rest_framework.views
from rest_framework import generics
from cart.models import Cart
from store.models import Product, Category
from store.utils import query_search
from . import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


# PRODUCT PRODUCT PRODUCT PRODUCT PRODUCT PRODUCT PRODUCT PRODUCT PRODUCT
class ProductLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 501
    default_limit = 20


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductLimitOffsetPagination

    def get_queryset(self):
        category_slug = self.request.GET.get('category_slug')
        discount = self.request.GET.get('discount')
        order_by_price = self.request.GET.get('order_by_price')
        query = self.request.GET.get('q')

        products = Product.objects.filter(quantity__gte=1)

        if category_slug:
            products = products.filter(category__category_slug=category_slug)

        if query:
            products = query_search(query, products, api=True)

        if discount:
            products = products.filter(discount__gt=0)

        if order_by_price and order_by_price != 'default':
            products = products.order_by(order_by_price)

        return products


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.order_by('-id')
    serializer_class = serializers.ProductSerializer
    lookup_field = 'pk'


# CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY
class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.order_by('name')


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.order_by('name')
    lookup_field = 'pk'


# CART CART CART CART CART CART CART CART CART CART CART CART CART CART CART CART
class CartListCreateDestroy(generics.ListCreateAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def delete(self, request):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return rest_framework.views.APIView.http_method_not_allowed(self, request)
