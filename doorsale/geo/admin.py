from django.contrib import admin

from doorsale.geo import models
from doorsale.admin import ModelAdmin


class CountryAdmin(ModelAdmin):
    list_display = ('name', 'iso_code2', 'iso_code3', 'iso_numeric', 'allow_billing', 'allow_shipping', 'subject_to_vat', 'display_order', 'is_active',)
    list_filter = ('is_active', 'allow_billing', 'allow_shipping', 'subject_to_vat', 'display_order', 'created_on',)
    search_fields = ('name', 'iso_code2', 'iso_code3', 'iso_numeric',)
    date_hierarchy = 'created_on'


class StateAdmin(ModelAdmin):
    list_display = ('name', 'code', 'country', 'display_order', 'is_active',)
    list_filter = ('is_active', 'display_order', 'created_on',)
    search_fields = ('name', 'code', 'country__name',)
    date_hierarchy = 'created_on'



admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.State, StateAdmin)