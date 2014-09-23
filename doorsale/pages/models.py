from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class FlatPage(models.Model):
    """
    Represents a static web page
    """
    PAGE_VIEWS = (('pages_base_page', 'Base View'),
                  ('pages_catalog_page', 'Catalog View'))

    title = models.CharField(max_length=200)
    url = models.SlugField(max_length=100, unique=True)
    content = models.TextField(blank=True)
    render_view = models.CharField(max_length=100, choices=PAGE_VIEWS,
                                   help_text='Render page in base template or catalog template.')
    is_active = models.BooleanField()
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Flat page'
        verbose_name_plural = 'Flat Pages'
        ordering = ('url',)

    @models.permalink
    def get_absolute_url(self):
        return (self.render_view, (self.url,))


class Article(models.Model):
    """
    Article represents page, blog post or content representing pages or post
    """

    TYPE_PAGE = 'PA'
    TYPE_POST = 'PO'
    TYPE_CONTENT = 'CO'

    TYPES = ((TYPE_PAGE, 'Page'),
             (TYPE_POST, 'Post'),
             (TYPE_CONTENT, 'Content'),)

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
    excerpt = models.TextField(blank=True,
                               help_text='Content excerpt (optional)')
    status = models.CharField(max_length=2, choices=STATUSES, default=STATUS_DRAFT)
    tags = models.CharField(max_length=255, blank=True, help_text='Tags for the published article')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    published = models.DateTimeField('published date', blank=True, null=True)
    created_on = models.DateTimeField('creation date', auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField('last updated', auto_now=True)
    updated_by = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s -- %s" % (self.url, self.title)

    def is_published(self):
        return self.status == self.STATUS_PUBLISHED


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
            raise ValidationError('You must specify either flat page resource or any'
                                  ' other url resource this link points to.')
