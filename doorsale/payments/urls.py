from django.conf.urls import patterns, url

from doorsale.payments.views import online_payment, credit_card_payment, account_payment

urlpatterns = patterns('',
    url(r'^online_payment/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$', online_payment, name='payments_online_payment'),
    url(r'^credit_card_payment/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$', credit_card_payment, name='payments_credit_card_payment'),
    url(r'^account_payment/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$', credit_card_payment, name='payments_account_payment'),
)