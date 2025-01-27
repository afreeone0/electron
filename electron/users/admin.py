from django.contrib import admin
from .models import User
from store.admin import CartAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    ordering = ('first_name',)
    inlines = (CartAdmin,)
