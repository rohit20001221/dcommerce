from django.contrib import admin
from .models import Cart, CartItem, Order
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
