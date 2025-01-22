from django.db import models
from users.models import User
from operator import add
from functools import reduce


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    category_slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.discount:
            return self.price / 100 * (100 - self.discount)

        return self.price


class Cart(models.Model):
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price_for_user(self):
        user_carts = Cart.objects.filter(user=self.user)
        return reduce(add, map(lambda crt: crt.quantity * crt.product.price, user_carts))
