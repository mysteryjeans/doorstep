from django.contrib import admin

from doorsale.admin import ModelAdmin
from doorsale.payments.models import Gateway, GatewayParam, Transaction, TransactionParam


class GatewayAdmin(ModelAdmin):
    list_display = ('name', 'account_name', 'is_active',)
    list_filter = ('name',)
    search_fields = ('name', 'account_name',)
    date_hierarchy = 'created_on'


class GatewayParamAdmin(ModelAdmin):
    list_display = ('gateway', 'name',)
    list_filter = ('gateway', 'name',)
    search_fields = ('gateway', 'name',)
    date_hierarchy = 'created_on'


class TransactionAdmin(ModelAdmin):
    list_display = ('gateway', 'order', 'stan', 'status', 'amount',)
    list_filter = ('gateway', 'status',)
    search_fields = ('gateway', 'order', 'stan', 'sale_id',)
    date_hierarchy = 'created_on'


class TransactionParamAdmin(ModelAdmin):
    list_display = ('transaction', 'name', 'value')
    list_filter = ('name',)
    search_fields = ('transaction', 'name', 'value',)
    date_hierarchy = 'created_on'


admin.site.register(Gateway, GatewayAdmin)
admin.site.register(GatewayParam, GatewayParamAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionParam, TransactionParamAdmin)