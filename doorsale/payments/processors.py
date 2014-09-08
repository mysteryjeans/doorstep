from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from doorsale.payments.models import Gateway, Transaction, TransactionParam

# Processors module logger
logger = logging.getLogger('django.request')


class PayPal:
    """
    Represents PayPal gateway for processing payments
    """
    import paypalrestsdk

    def __init__(self):
        self.mode = 'sandbox' if settings.DEBUG else 'live'
        
        try:
            self.gateway = Gateway.objects.get(name=Gateway.PAYPAL)
        except Gateway.DoesNotExists:
            raise ImproperlyConfigured('Paypal gateway is not configured or inactive, please use admin to configure Paypal API settings through gateway.')

        params = dict((param.name, param.value) for param in self.gateway.params.all())
        
        if 'client_id' in params and not params['client_id']:
            client_id = params['client_id']
        else:
            raise ImproperlyConfigured('"client_id" parameter not configured for PayPal gateway "%s".' % self.gateway)
        
        if 'client_secret' in params and not params['client_secret']:
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
                    'currency': order.currency,
                    'details': {
                        'subtotal': unicode(order.sub_total),
                        'tax': unicode(order.taxes),
                        'shipping': unicode(order.shipping_cost)
                        }
                    },
                'description': 'Payment for order #%s' % (order.id)
                }],
            }, api=self.api)

        transaction = Transaction.objects.create(gateway=self.gateway,
                                                 order=order,
                                                 description='Transaction for order #%' % order.id,
                                                 status=Transaction.STATUS_PROCESSING,
                                                 currency=order.currency,
                                                 amount=order.total,
                                                 updated_by=unicode(user),
                                                 created_by=unicode(user))

        if payment.create():
            transaction.status = Transaction.STATUS_APPROVED
            # Saving only few necessary fields
            transaction.add_param(name='id', value=unicode(payment.id), user)
            transaction.add_param(name='create_time', value=unicode(payment.create_time), user)
            transaction.add_param(name='update_time', value=unicode(payment.update_time), user)
            transaction.add_param(name='state', value=unicode(payment.state), user)
            transaction.add_param(name='intent', value=unicode(payment.intent), user)
            transaction.add_param(name='payment_method', value=unicode(payment.payer.payment_method), user)
            transaction.add_param(name='sale_id', value=unicode(payment.transactions[0].related_resources[0].sale.id), user)
            transaction.save()
        else:
            logger.error("Failed to process Paypal payment transaction: %s\n%s", transaction.id, payment.error)
            transaction.status = Transaction.STATUS_FAILED
            transaction.error_message = payment.error.message
            transaction.add_param(name='id', value=unicode(payment.id), user)
            transaction.save()
            raise DoorsaleError(transaction.error_message)

        return transaction

    def refund_payment(self):
        """
        Refunds an transaction amount
        """
        