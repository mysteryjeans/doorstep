from django.contrib import admin

from doorsale.admin import ModelAdmin
from doorsale.pages.models import FlatPage, Link


class FlatPageAdmin(ModelAdmin):
    list_display = ('url', 'title', 'is_active', 'render_view')
    list_filter = ('is_active', 'render_view')
    search_fields = ('url', 'title',)
    prepopulated_fields = {"url": ("title",)}
    date_hierarchy = 'created_on'


class LinkAdmin(ModelAdmin):
    list_display = ('name', 'group', 'page', 'url')
    list_filter = ('group',)
    search_fields = ('name', 'group', 'page__name',)
    date_hierarchy = 'created_on'


admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Link, LinkAdmin)
