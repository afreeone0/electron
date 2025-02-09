import rest_framework.views
from rest_framework import generics
from cart.models import Cart
from store.models import Product, Category
from orders.models import Order
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


# CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY CATEGORY
class CategoryListCreate(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.order_by('name')


class CategoryRetrieve(generics.RetrieveAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.order_by('name')


# CART CART CART CART CART CART CART CART CART CART CART CART CART CART CART CART
class CartListCreateDestroy(generics.ListCreateAPIView):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).order_by('product__id')

        return Cart.objects.filter(session_key=self.request.session.session_key).order_by('product__id')

    def delete(self, request):
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


# ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS ORDERS
class OrderListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
