from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.flatpages.models import FlatPage


class FlatPage(models.Model):
    """
    Represents a static web page
    """
    PAGE_VIEWS = (('pages_base_page', 'Base View'),
                  ('pages_catalog_page', 'Catalog View'))
    
    title = models.CharField(max_length=200)
    url = models.SlugField(max_length=100, unique=True)
    content = models.TextField(blank=True)
    render_view = models.CharField(max_length=100, choices=PAGE_VIEWS, help_text='Render page in base template or catalog template.')
    is_active = models.BooleanField()
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Flat page'
        verbose_name_plural = 'Flat Pages'
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    @models.permalink
    def get_absolute_url(self):
        return (self.render_view, (self.url,))


class Link(models.Model):
    """
    Represents a link resource to listings
    """
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=100, help_text='Group text under which links will be compiled for display.')
    url = models.CharField(max_length=500, blank=True, null=True, help_text='Url of resource this link points to.')
    page = models.ForeignKey(FlatPage, blank=True, null=True, help_text='Flat page resource this link points to.')
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def clean(self):
        # Link resource must points to either flat page resource or any other url resource
        if not (self.url or self.page):
            raise ValidationError('You must specify either flat page resource or any other url resource this link points to.')



