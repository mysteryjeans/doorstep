from __future__ import unicode_literals

import logging

# Payment gateway SDKs
import stripe
import paypalrestsdk

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from doorsale.exceptions import DoorsaleError
from doorsale.sales.models import Order
from doorsale.payments.models import Gateway, GatewayParam, Transaction, TransactionParam

# Processors module logger
logger = logging.getLogger('django.request')


class PayPal:
    """
    PayPal gateway for processing payments
    """
    def __init__(self, gateway):
        self.gateway = gateway
        self.mode = 'sandbox' if gateway.is_sandbox else 'live'
        
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
    
    def account_payment(self, **kwargs):
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
                        'expire_month': unicode(card['expire_month']),
                        'expire_year': unicode(card['expire_year']),
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

        try:
            payment_created = payment.create()
        except Exception as e:
            logger.error('Failed to process Credit Card (transaction_id: %s)' % payment_txn.id)
            logger.exception(e)

            raise DoorsaleError('We failed to process your Credit Card at the moment, please try again later!')

        if payment_created:
            try:
                with transaction.atomic():
                    # Saving only few necessary fields refunding & record
                    payment_txn.status = Transaction.STATUS_APPROVED
                    payment_txn.add_param('id', unicode(payment.id), user)
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
                logger.error('Failed to save successful Credit Card payment (transaction_id: %s, payment_id: %s) in database.' % (payment_txn.id, payment.id))
                raise e
        else:
            logger.error('Failed to process Credit Card (transaction_id: %s)' % payment_txn.id, extra={ 'error': payment.error })

            with transaction.atomic():
                payment_txn.status = Transaction.STATUS_FAILED
                dir(payment.error)
                print payment.error
                payment_txn.error_message = payment.error['message']
                payment_txn.save()

            raise DoorsaleError('We failed to process your Credit Card at the moment, please try again later!')

        return payment_txn

    def refund_payment(self, **kwargs):
        """
        Refunds an transaction amount
        """


class Stripe:
    """
    Stripe gateway for processing payments
    """
    def __init__(self, gateway):
        self.gateway = gateway

        try:
            api_key = gateway.params.get(name='api_key')
        except GatewayParam.DoesNotExist:
            raise ImproperlyConfigured('"api_key" parameter not configured for Strip gateway "%s".' % self.gateway)

        self.api_key = api_key.value

        # Verifying api_key configured according to sandbox or live mode
        if gateway.is_sandbox:
            if self.api_key.startswith('sk_live'):
                raise ImproperlyConfigured('"%s" Gateway is configured for sandbox mode but uses live "api_key".' % self.gateway)
        else:
            if self.api_key.startswith('sk_test'):
                raise ImproperlyConfigured('"%s" Gateway is configured for live mode but uses test "api_key".' % self.gateway)

        stripe.api_key = self.api_key

    def account_payment(self, **kwargs):
        """
        Payment transaction of Strip account
        """

    def credit_card_payment(self, card, order, user):
        """
        Payment transaction of credit card from Strip gateway
        """
        with transaction.atomic():
            payment_txn = Transaction.objects.create(gateway=self.gateway,
                                                     order=order,
                                                     description='Transaction for order #%s' % order.id,
                                                     status=Transaction.STATUS_PROCESSING,
                                                     currency=order.currency.code,
                                                     amount=order.total,
                                                     updated_by=unicode(user),
                                                     created_by=unicode(user))
        try:
            charge = stripe.Charge.create(
                amount=int(order.total * 100), # 100 cents to charge $1.00
                currency=order.currency.code.lower(),
                description='Payment for order #%s' % (order.id),
                card={
                    'number': card['number'],
                    'name': card['name'],
                    'exp_month': card['expire_month'],
                    'exp_year': card['expire_year'],
                    'cvc': card['cvv2']
                })

            with transaction.atomic():
                # Saving only few necessary fields for refunding
                payment_txn.status = Transaction.STATUS_APPROVED
                payment_txn.add_param('id', unicode(charge.id), user)
                payment_txn.add_param('created', unicode(charge.created), user)
                payment_txn.add_param('amount', unicode(charge.amount), user)
                payment_txn.add_param('card_id', unicode(charge.card.id), user)
                payment_txn.add_param('card_last4', unicode(charge.card.last4), user)
                payment_txn.add_param('card_country', unicode(charge.card.country), user)
                payment_txn.add_param('card_brand', unicode(charge.card.brand), user)
                payment_txn.save()

                order.payment_status = Order.PAYMENT_PAID
                order.updated_by = unicode(user)
                order.save()

        except stripe.error.CardError as e:
            # The card has been declined
            body = e.json_body
            error = body['error'] 
            logger.warning('Credit Card has been declined (transaction_id: %s)' % payment_txn.id, extra=error)

            payment_txn.status = Transaction.STATUS_FAILED
            payment_txn.error_message = error['message']
            payment_txn.save()

            raise DoorsaleError(error['message'])
        except Exception as e:
            logger.error('Failed to process Credit Card (transaction_id: %s)' % payment_txn.id)
            logger.exception(e)
        
            raise DoorsaleError('We failed to process your Credit Card at the moment, please try again later!')

    def refund_payment(self, **kwargs):
        """
        Refunds an transaction amount
        """

        