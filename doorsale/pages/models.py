from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError


class Page(models.Model):
    """
    Article represents page, blog post or content representing pages or post
    """

    STATUS_DRAFT = 'DR'
    STATUS_WITHDRAWN = 'WD'
    STATUS_PUBLISHED = 'PU'

    STATUSES = ((STATUS_DRAFT, 'Draft'),
                (STATUS_WITHDRAWN, 'Withdrawn'),
                (STATUS_PUBLISHED, 'Published'),)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255,
                            help_text='Title text to be used in url for this post')
    content = models.TextField()
    status = models.CharField(max_length=2, choices=STATUSES, default=STATUS_DRAFT)
    tags = models.CharField(max_length=255, null=True, blank=True, help_text='Tags for the published article')
    published = models.DateTimeField('published date', blank=True, null=True)
    created_on = models.DateTimeField('creation date', auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField('last updated', auto_now=True)
    updated_by = models.CharField(max_length=100)

    class Meta:
        ordering = ('slug',)

    def __unicode__(self):
        return "%s -- %s" % (self.slug, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('pages_page_view', (self.slug,))

    def is_published(self):
        return self.status == self.STATUS_PUBLISHED

    def clean(self):
        if self.status == self.STATUS_PUBLISHED and self.published is None:
            raise ValidationError('Published date not specified.')


class Link(models.Model):
    """
    Represents a link resource to listings
    """
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=100, help_text='Group text under which links will be compiled for display.')
    url = models.CharField(max_length=500, blank=True, null=True, help_text='Url of resource this link points to.')
    page = models.ForeignKey(Page, blank=True, null=True, help_text='Page resource this link points to.')
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def clean(self):
        # Link resource must points to either flat page resource or any other url resource
        if not (self.url or self.page):
            raise ValidationError('You must specify either flat page resource or any'
                                  ' other url resource this link points to.')
