from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_slug')
    fields = ('name', 'category_slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'category_slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'product_slug')
    prepopulated_fields = {'product_slug': ('name',)}
    search_fields = ('name', 'price')
    ordering = ('-price',)
