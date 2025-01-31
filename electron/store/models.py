from django.db import models


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

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    product_slug = models.SlugField(max_length=40, unique=True, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.discount:
            return round(self.price / 100 * (100 - self.discount), 2)

        return self.price
