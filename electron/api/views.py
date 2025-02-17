from django.contrib import auth
from rest_framework import views
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

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


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user).order_by('product__id')

        if not self.request.session.session_key:
            self.request.session.create()

        return Cart.objects.filter(session_key=self.request.session.session_key).order_by('product__id')

    def create(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        if not (request.user.is_authenticated or request.session.session_key):
            request.session.create()
        session_key = request.session.session_key if request.session.session_key else None

        data = request.data
        product, quantity = data.get('product'), data.get('quantity')
        if not (product and quantity):
            return Response({'error': 'product and quantity fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_obj = Product.objects.get(pk=product)
        except Product.DoesNotExist:
            return Response({'error': 'there is no product with such id'})

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({'error': 'quantity must be positive integer'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'quantity must be a number'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = Cart.add_to_cart(user=user, session_key=session_key, product=product_obj, quantity=quantity)
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False, url_path='all')
    def destroy_all(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class LoginAPIView(views.APIView):
    def post(self, request):
        session_key = request.session.session_key
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(created)
            auth.login(request, user)
            if session_key:
                for cart_not_auth in Cart.objects.filter(session_key=session_key):
                    cart_auth = Cart.objects.filter(user=user, product=cart_not_auth.product).first()
                    if cart_auth:
                        cart_auth.quantity += cart_not_auth.quantity
                        cart_auth.save()
                    else:
                        cart_not_auth.user = user
                        cart_not_auth.save()
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
