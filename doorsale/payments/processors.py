from __future__ import unicode_literals

import logging

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from doorsale.exceptions import DoorsaleError
from doorsale.sales.models import Order
from doorsale.payments.models import Gateway, Transaction, TransactionParam

# Processors module logger
logger = logging.getLogger('django.request')


class PayPal:
    """
    Represents PayPal gateway for processing payments
    """
    def __init__(self):
        import paypalrestsdk

        self.mode = 'sandbox' if settings.DEBUG else 'live'
        
        try:
            self.gateway = Gateway.objects.get(name=Gateway.PAYPAL)
        except Gateway.DoesNotExists:
            raise ImproperlyConfigured('PayPal gateway is not configured or inactive, please use admin to configure Paypal API settings through gateway.')

        params = dict((param.name, param.value) for param in self.gateway.params.all())
        
        if 'client_id' in params and params['client_id']:
            client_id = params['client_id']
        else:
            raise ImproperlyConfigured('"client_id" parameter not configured for PayPal gateway "%s".' % self.gateway)
        
        if 'client_secret' in params and params['client_secret']:
            client_secret = params['client_secret']
        else:
            raise ImproperlyConfigured('"client_secret" parameter not configured for PayPal gateway "%s".' % self.gateway)

        self.api = paypalrestsdk.Api({
            'mode': self.mode,
            'client_id': client_id,
            'client_secret': client_secret
            })
    
    def paypal_payment(self):
        """
        Payment transaction from PayPal account
        """
    
    def credit_card_payment(self, card, order, user):
        """
        Payment transaction of credit card from PayPal gateway
        """
        import paypalrestsdk

        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {
                'payment_method': 'credit_card',
                'funding_instruments': [{
                    'credit_card': {
                        'type': card['type'],
                        'number': card['number'],
                        'expire_month': card['expire_month'],
                        'expire_year': card['expire_year'],
                        'cvv2': card['cvv2'],
                        'first_name': card['first_name'],
                        'last_name': card['last_name']
                        }
                    }]
                },
            'transactions': [{
                'amount': {
                    'total': unicode(order.total),
                    'currency': order.currency.code,
                    'details': {
                        'subtotal': unicode(order.sub_total),
                        'tax': unicode(order.taxes),
                        'shipping': unicode(order.shipping_cost)
                        }
                    },
                'description': 'Payment for order #%s' % (order.id)
                }],
            }, api=self.api)
        
        with transaction.atomic():
            payment_txn = Transaction.objects.create(gateway=self.gateway,
                                                     order=order,
                                                     description='Transaction for order #%s' % order.id,
                                                     status=Transaction.STATUS_PROCESSING,
                                                     currency=order.currency.code,
                                                     amount=order.total,
                                                     updated_by=unicode(user),
                                                     created_by=unicode(user))

        if payment.create():
            try:
                with transaction.atomic():
                    # Saving only few necessary fields refunding & record
                    payment_txn.status = Transaction.STATUS_APPROVED
                    payment_txn.add_param('payment_id', unicode(payment.id), user)
                    payment_txn.add_param('create_time', unicode(payment.create_time), user)
                    payment_txn.add_param('update_time', unicode(payment.update_time), user)
                    payment_txn.add_param('state', unicode(payment.state), user)
                    payment_txn.add_param('intent', unicode(payment.intent), user)
                    payment_txn.add_param('payment_method', unicode(payment.payer.payment_method), user)
                    payment_txn.add_param('sale_id', unicode(payment.transactions[0].related_resources[0].sale.id), user)
                    payment_txn.save()

                    order.payment_status = Order.PAYMENT_PAID
                    order.updated_by = unicode(user)
                    order.save()
            except Exception as e:
                logger.warning('Failed to save successful PayPal payment transaction (transaction_id: %s, payment_id: %s) in database.' % (payment_txn.id, payment.id))
                raise e
        else:
            logger.error('Failed to process PayPal payment (transaction_id: %s)' % payment_txn.id, extra={ 'error': payment.error })

            with transaction.atomic():
                payment_txn.status = Transaction.STATUS_FAILED
                dir(payment.error)
                print payment.error
                payment_txn.error_message = payment.error['message']
                payment_txn.save()

            raise DoorsaleError('We failed to process your credit card, sorry for the inconvenience!')

        return payment_txn

    def refund_payment(self):
        """
        Refunds an transaction amount
        """
        