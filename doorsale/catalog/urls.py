from django.conf.urls import patterns, url

from doorsale.catalog.views import IndexView, ProductListView, ProductDetailView

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='catalog_index'),
                       url(r'^categories/(?P<slug>[\w-]+)/$', ProductListView.as_view(), name='catalog_category_products'),
                       url(r'^products/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='catalog_product'),
)
