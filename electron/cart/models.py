from django.db import models
from users.models import User
from store.models import Product


class CartQuerySet(models.QuerySet):
    def get_total_price_for_user(self):
        return sum(cart.get_price_for_product() for cart in self)

    def get_total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)

        return 0


class Cart(models.Model):
    objects = CartQuerySet().as_manager()

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def get_price_for_product(self):
        return self.product.get_price() * self.quantity

    @classmethod
    def add_to_cart(cls, product, quantity, user=None, session_key=None):
        try:
            cart_item = cls.objects.get(user=user, session_key=session_key, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        except cls.DoesNotExist:
            cart_item = cls(user=user, session_key=session_key, product=product, quantity=quantity)
            cart_item.save()
            return cart_item
