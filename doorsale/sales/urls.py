from django.conf.urls import patterns, url

from doorsale.sales.views import add_to_cart, remove_from_cart, remove_all_from_cart
from doorsale.sales.views import CheckoutCartView, CheckoutBillingView, CheckoutShippingView, CheckoutPaymentView, CheckoutOrderView, CheckoutReceiptView

urlpatterns = patterns('',
                       url(r'^cart/add/$', add_to_cart, name='sales_add_to_cart'),
                       url(r'^cart/remove/$', remove_from_cart, name='sales_remove_from_cart'),
                       url(r'^cart/remove/all$', remove_all_from_cart, name='sales_remove_all_from_cart'),
                       url(r'^checkout/cart/$', CheckoutCartView.as_view(), name='sales_checkout_cart'),
                       url(r'^checkout/billing/$', CheckoutBillingView.as_view(), name='sales_checkout_billing'),
                       url(r'^checkout/shipping/$', CheckoutShippingView.as_view(), name='sales_checkout_shipping'),
                       url(r'^checkout/payment/$', CheckoutPaymentView.as_view(), name='sales_checkout_payment'),
                       url(r'^checkout/order/$', CheckoutOrderView.as_view(), name='sales_checkout_order'),
                       url(r'^checkout/receipt/$', CheckoutReceiptView.as_view(), name='sales_checkout_receipt'),
)