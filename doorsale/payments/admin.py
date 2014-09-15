from django.contrib import admin

from doorsale.admin import ModelAdmin
from doorsale.payments.models import CardIssuer, Gateway, GatewayParam, Transaction, TransactionParam


class CardIssuerAdmin(ModelAdmin):
    list_display = ('descriptor', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('descriptor', 'name',)
    date_hierarchy = 'created_on'


class GatewayAdmin(ModelAdmin):
    list_display = ('name', 'account', 'is_active',)
    list_filter = ('account',)
    search_fields = ('name', 'account',)
    date_hierarchy = 'created_on'


class GatewayParamAdmin(ModelAdmin):
    list_display = ('name', 'value', 'gateway')
    list_filter = ('gateway__name', 'name',)
    search_fields = ('gateway', 'name',)
    date_hierarchy = 'created_on'


class TransactionAdmin(ModelAdmin):
    list_display = ('id', 'order', 'status', 'amount', 'currency')
    list_filter = ('gateway__name', 'status',)
    search_fields = ('id', 'order', 'gateway__name',)
    date_hierarchy = 'created_on'


class TransactionParamAdmin(ModelAdmin):
    list_display = ('transaction', 'name', 'value')
    list_filter = ('name',)
    search_fields = ('transaction__id', 'name', 'value',)
    date_hierarchy = 'created_on'


admin.site.register(CardIssuer, CardIssuerAdmin)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(GatewayParam, GatewayParamAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TransactionParam, TransactionParamAdmin)