from django.contrib import admin
from .models import AppCategory, AppProduct, Order, Cart, CartItem, OrderItem


admin.site.register(AppCategory)
admin.site.register(AppProduct)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
