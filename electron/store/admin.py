from django.contrib import admin
from .models import Category, Product, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_slug')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name', 'price')
    ordering = ('-price',)


class CartAdmin(admin.TabularInline):
    model = Cart
    fields = ('user', 'product', 'quantity')
    extra = 0
