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
    name = serializers.CharField(read_only=True, max_length=150)
    price = serializers.DecimalField(read_only=True, max_digits=13, decimal_places=2)

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

    def create(self, validated_data):
        orderItems_data = validated_data.pop('orderItems')
        order = Order.objects.create(**validated_data)
        for orderItem_data in orderItems_data:
            product = Product.objects.get(pk=orderItem_data['product'].pk)
            orderItem_data['name'] = product.name
            orderItem_data['price'] = product.get_price()
            OrderItem.objects.create(order=order, **orderItem_data)
        return order
