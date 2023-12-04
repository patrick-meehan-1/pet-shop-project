from django.contrib import admin
from .models import Cart, CartItem, Checkout, OrderItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart_id', 'date_added')
    list_filter = ('date_added', 'user')
    search_fields = ('cart_id', 'user__username')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'active')
    list_filter = ('active', 'cart')
    search_fields = ('cart__cart_id', 'product__name')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']  
    list_filter = ['order']
    search_fields = ['order__id', 'product__name']

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'payment_method', 'order_total', 'created_at')
    list_filter = ('created_at', 'user', 'payment_method')
    search_fields = ('id', 'user__username', 'shipping_address')





admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Checkout, CheckoutAdmin)

