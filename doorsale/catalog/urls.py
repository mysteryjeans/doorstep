from django.conf.urls import patterns, include, url

urlpatterns = patterns('doorsale.catalog.views',
                       url(r'^$', 'index', name='catalog_index'),
                       url(r'^categories/(?P<slug>[\w-]+)/$', 'category_products', name='catalog_category_products'),
)
