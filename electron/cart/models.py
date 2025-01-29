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
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def get_price_for_product(self):
        return round(self.product.get_price() * self.quantity, 2)

    objects = CartQuerySet().as_manager()
