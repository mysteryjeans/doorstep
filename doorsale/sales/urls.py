from django.conf.urls import patterns, url

from doorsale.sales.views import add_to_cart

urlpatterns = patterns('',
                       url(r'^cart/add/$', add_to_cart, name='sales_add_to_cart'),
)