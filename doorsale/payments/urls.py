from django.conf.urls import patterns, url

from doorsale.payments.views import process_online, process_credit_card, \
    process_account_request, process_account_response, ProcessingMessageView

urlpatterns = patterns('',
                       url(r'^process_online/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$',
                           process_online, name='payments_process_online'),
                       url(r'^process_credit_card/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$',
                           process_credit_card, name='payments_process_credit_card'),
                       url(r'^process_account/request/(?P<order_id>\d+)-(?P<receipt_code>\w+)/$',
                           process_account_request, name='payments_process_account_request'),
                       url(r'^process_account/success/(?P<transaction_id>\d+)-(?P<access_token>\w+)/$',
                           process_account_response, {'success': True}, name='payments_process_account_success'),
                       url(r'^process_account/cancel/(?P<transaction_id>\d+)-(?P<access_token>\w+)/$',
                           process_account_response, {'success': False}, name='payments_process_account_cancel'),
                       url(r'^processing_message/$', ProcessingMessageView.as_view(),
                           name='payments_processing_message'),
                       )
