from django.conf.urls import patterns, url

from doorsale.catalog.views import *

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='catalog_index'),
                       url(r'^categories/(?P<slug>[\w-]+)/$', CategoryProductsView.as_view(),
                           name='catalog_category_products'),
                       url(r'^manufacturers/(?P<slug>[\w-]+)/$', ManufacturerProductsView.as_view(),
                           name='catalog_manufacturer_products'),
                       url(r'^search/$', SearchProductsView.as_view(),
                           name='catalog_search_products'),
                       url(r'^search/$', SearchProductsView.as_view(),
                           name='catalog_search_advance_products'),
                       url(r'^products/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='catalog_product'),
)
