from django.conf.urls import patterns, url

from doorsale.payments.views import paypal_success, paypal_cancel

urlpatterns = patterns('',
                       url(r'^paypal/success/(?P<order_id>\d+)/$', paypal_success, name='payments_paypal_success'),
                       url(r'^paypal/cancel/(?P<order_id>\d+)/$', paypal_cancel, name='payments_paypal_cancel'),
)