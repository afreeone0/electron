from rest_framework import serializers
from cart.models import Cart
from store.models import Product, Category
from orders.models import Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('created_timestamp', 'order')


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "phone_number",
            "created_timestamp",
            "requires_delivery",
            "delivery_address",
            "payment_on_get",
            "is_paid",
            "status",
            "orderItems",
        )
