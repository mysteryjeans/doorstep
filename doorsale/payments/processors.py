from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from doorsale.payments.models import Gateway


class PayPal:
    """
    Represents PayPal gateway for processing payments
    """
    def __init__(self):
        self.mode = 'sandbox' if settings.DEBUG else 'live'
        
        try:
            gateway = Gateway.objects.get(name=Gateway.PAYPAL)
            self.account = gateway.account_name
        except Gateway.DoesNotExist:
            raise ImproperlyConfigured('Paypal gateway is not configured, please use admin to configure Paypal API settings through gateway.')
        
        params = dict((param.name, param.value) for param in gateway.params.all())
        
        if 'client_id' in params and not params['client_id']:
            self.client_id = params['client_id']
        else:
            raise ImproperlyConfigured('client_id parameter not configured for PayPal gateway.')
        
        if 'client_secret' in params and not params['client_secret']:
            self.client_secret = params['client_secret']
        else:
            raise ImproperlyConfigured('client_secret parameter not configured for PayPal gateway.')
    
    def create_payment_paypal(self):
        """
        Payment transaction from PayPal account
        """
    
    def create_payment_credit_card(self):
        """
        Payment transaction of credit card from PayPal gateway
        """
        
    def refuned_payment(self):
        """
        Refunds an transaction amount
        """
        