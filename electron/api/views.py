import rest_framework.views
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

from . import serializers
from store.utils import query_search

from cart.models import Cart
from store.models import Product, Category
from orders.models import Order


class ProductLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 501
    default_limit = 20


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
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


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.order_by('name')


class CartListCreateDestroy(mixins.ListModelMixin,
                            generics.GenericAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).order_by('product__id')

        return Cart.objects.filter(session_key=self.request.session.session_key).order_by('product__id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        if not (request.session.session_key or request.user.is_authenticated):
            request.session.create()

        if not request.user.is_authenticated:
            request.data['session_key'] = request.session.session_key
        else:
            request.data['user'] = request.user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).order_by('product__id')

        if not self.request.session.session_key:
            self.request.session.create()

        return Cart.objects.filter(session_key=self.request.session.session_key).order_by('product__id')

    def put(self, request, *args, **kwargs):
        return rest_framework.views.APIView.http_method_not_allowed(self, request)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
