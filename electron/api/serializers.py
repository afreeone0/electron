from rest_framework import serializers
from django.core.exceptions import ValidationError
from cart.models import Cart
from store.models import Product, Category
from orders.models import Order, OrderItem
from users.models import User
from validators import get_validators_list


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'image', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}},
            'phone_number': {'required': False},
            'image': {'required': False},
            'username': {'read_only': True}
        }

    def validate_image(self, image):
        try:
            for validator in get_validators_list():
                    validator(image)
        except ValidationError as ve:
            raise serializers.ValidationError(str(ve))
        return image

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def validate(self, data):
        if data['password1'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
