from django.contrib import admin
from .models import Cart


class CartAdmin(admin.TabularInline):
    model = Cart
    fields = ('user', 'product', 'quantity')
    extra = 0
