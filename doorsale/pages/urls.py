from django.conf.urls import patterns, url

from doorsale.pages.views import BasePageView, CatalogPageView

urlpatterns = patterns('',
    url(r'^base/(?P<page_url>[\w-]+)/$', BasePageView.as_view(), name='pages_base_page'),
    url(r'^catalog/(?P<page_url>[\w-]+)/$', CatalogPageView.as_view(), name='pages_catalog_page'),
)