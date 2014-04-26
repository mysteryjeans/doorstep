from django.contrib import admin

from doorsale.admin import ModelAdmin
from doorsale.common import models


class AddressAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'address1', 'address2', 'city', 'state', 'country',)
    list_filter = ('city', 'state', 'country', 'created_on',)
    search_fields = ('first_name', 'last_name', 'email', 'address1', 'address2',)
    date_hierarchy = 'created_on'


class UserAdmin(ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'gender', 'is_verified',)
    list_filter = ('gender', 'created_on',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    date_hierarchy = 'created_on'


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.User, UserAdmin)