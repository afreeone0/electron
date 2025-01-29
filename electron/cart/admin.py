from django.contrib import admin
from .models import Cart


class CartAdmin(admin.TabularInline):
    model = Cart
    fields = ('user', 'product', 'quantity', 'session_key', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
