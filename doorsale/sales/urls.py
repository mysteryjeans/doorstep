from django.conf.urls import patterns, url

from doorsale.sales.views import add_to_cart, remove_from_cart

urlpatterns = patterns('',
                       url(r'^cart/add/$', add_to_cart, name='sales_add_to_cart'),
                       url(r'^cart/remove/$', remove_from_cart, name='sales_remove_from_cart'),
)