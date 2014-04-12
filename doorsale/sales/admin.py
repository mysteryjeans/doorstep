from django.contrib import admin

from . import models
from ..admin import ModelAdmin


class CartAdmin(ModelAdmin):
    list_display = ('id', 'updated_on', 'updated_by',)
    list_filter = ('created_on',)
    search_fields = ('id',)
    date_hierarchy = 'created_on'


class CartItemAdmin(ModelAdmin):
    list_display = ('product', 'cart', 'quantity',)
    list_filter = ('product', 'created_on',)
    search_fields = ('product', 'cart',)
    date_hierarchy = 'created_on'


class OrderAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'currency', 'sub_total', 'taxes', 'total', 'refunded_amount', 'payment_status', 'order_status', 'shipping_status', )
    list_filter = ('payment_status', 'order_status', 'shipping_status', 'currency', 'created_on',)
    search_fields = ('id', 'customer', 'currency',)
    date_hierarchy = 'created_on'


class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity', 'sub_total', 'taxes', 'total', 'tax_rate', 'tax_method', )
    list_filter = ('tax_rate', 'tax_method', 'created_on',)
    search_fields = ('order', 'product',)
    date_hierarchy = 'created_on'


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)