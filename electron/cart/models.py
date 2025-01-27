from django.db import models
from users.models import User
from store.models import Product
from operator import add
from functools import reduce


class Cart(models.Model):
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price_for_user(self):
        user_carts = Cart.objects.filter(user=self.user)
        return reduce(add, map(lambda crt: crt.quantity * crt.product.get_price(), user_carts))

