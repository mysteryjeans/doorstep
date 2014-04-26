from django.contrib import admin

from doorsale.admin import ModelAdmin 
from doorsale.catalog import models

class ManufacturerAdmin(ModelAdmin):
    list_display = ('name', 'description', 'is_active',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active', 'created_on',)
    search_fields = ('id', 'name', 'description',)
    date_hierarchy = 'created_on'


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent', 'tags', 'display_order', 'is_active',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent', 'created_on',)
    search_fields = ('name', 'description', 'tags',)
    date_hierarchy = 'created_on'


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'price', 'quantity', 'is_active', 'is_bestseller', 'is_featured',)
    list_filter = ('brand', 'is_active', 'is_bestseller', 'is_featured', 'is_free_shipping', 'created_on',)
    search_fields = ('name', 'gist', 'brand__name', 'sku', 'gtin', 'part_number',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_on'


class ProductSpecAdmin(ModelAdmin):
    list_display = ('product', 'name', 'value', 'display_order',)
    list_filter = ('name', 'created_on',)
    search_fields = ('name', 'value', 'product__name',)
    date_hierarchy = 'created_on'


class ProductPicAdmin(ModelAdmin):
    list_display = ('id', 'product', 'url', 'display_order',)
    list_filter = ('created_on',)
    search_fields = ('id', 'product__name', 'url',)
    date_hierarchy = 'created_on'


admin.site.register(models.Manufacturer, ManufacturerAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductSpec, ProductSpecAdmin)
admin.site.register(models.ProductPic, ProductPicAdmin)
