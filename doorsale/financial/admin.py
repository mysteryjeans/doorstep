from django.contrib import admin

from . import models
from ..admin import ModelAdmin


class CurrencyAdmin(ModelAdmin):
    list_display = ('name', 'code', 'exchange_rate', 'display_format', 'is_primary', 'is_active',)
    list_filter = ('is_primary', 'is_active', 'created_on',)
    search_fields = ('name', 'code',)
    date_hierarchy = 'created_on'


class TaxRateAdmin(ModelAdmin):
    list_display = ('name', 'method', 'rate',)
    list_filter = ('method', 'created_on',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'



admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.TaxRate, TaxRateAdmin)