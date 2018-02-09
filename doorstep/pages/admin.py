from django.contrib import admin

from doorstep.admin import ModelAdmin
from doorstep.pages.models import Page, Link


class PageAdmin(ModelAdmin):
    list_display = ('slug', 'title', 'status', 'published',)
    list_filter = ('status',)
    search_fields = ('slug', 'title',)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'created_on'


class LinkAdmin(ModelAdmin):
    list_display = ('name', 'group', 'page', 'url')
    list_filter = ('group',)
    search_fields = ('name', 'group', 'page__name',)
    date_hierarchy = 'created_on'


admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)
