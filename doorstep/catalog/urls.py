from django.conf.urls import url

from doorstep.catalog.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='catalog_index'),
    url(r'^categories/(?P<slug>[\w-]+)/$', CategoryProductsView.as_view(), {'page_num': 1}, name='catalog_category'),
    url(r'^categories/(?P<slug>[\w-]+)/(?P<page_num>\d+)/$', CategoryProductsView.as_view(), name='catalog_category'),
    url(r'^manufacturers/(?P<slug>[\w-]+)/$', ManufacturerProductsView.as_view(),
        {'page_num': 1}, name='catalog_manufacturer'),
    url(r'^manufacturers/(?P<slug>[\w-]+)/(?P<page_num>\d+)/$',
        ManufacturerProductsView.as_view(), name='catalog_manufacturer'),
    url(r'^search/$', SearchProductsView.as_view(), {'page_num': 1}, name='catalog_search'),
    url(r'^search/(?P<page_num>\d+)/$', SearchProductsView.as_view(), name='catalog_search'),
    url(r'^products/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='catalog_product'),
    url(r'^change_currency/$', ChangeCurrencyView.as_view(), name='catalog_change_currency'),
]
