from django.conf.urls import patterns, url

from .views import IndexView, ProductListView

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='catalog_index'),
                       url(r'^categories/(?P<slug>[\w-]+)/$', ProductListView.as_view(), name='catalog_category_products'),
)
