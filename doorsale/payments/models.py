from __future__ import unicode_literals

from django.db import models

from doorsale.sales.models import Order


class CardIssuer(models.Model):
    """
    Represents Credit Card Types
    """
    descriptor = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField()
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'payments_card_issuer'
        verbose_name_plural = 'Card Issuers'

    def __unicode__(self):
        return self.name


class Gateway(models.Model):
    """
    Represents payment processing gateways
    """
    PAYPAL = 'PP'
    AMAZON_PAYMENTS = 'AP'
    ALL = ((PAYPAL, 'PayPal'),
           (AMAZON_PAYMENTS, 'Amazon Payments'))
    
    name = models.CharField(primary_key=True, max_length=10, choices=ALL, help_text='Payment processing gateway.')
    account = models.CharField(max_length=100, help_text='Payment account name, usually it is your configured business email address of your merchant account.')
    is_active = models.BooleanField(help_text='Gateway active for customer to buy through it.')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.account

    @classmethod
    def get_gateways(cls):
        """
        Returns list of active gateways
        """
        return list(cls.objects.filter(is_active=True))


class GatewayParam(models.Model):
    """
    Represents a payment processing gateway settings
    """
    gateway = models.ForeignKey(Gateway, related_name='params')
    name = models.CharField(max_length=250, help_text='Gateway settings parameter name.')
    value = models.CharField(max_length=500, help_text='Gateway settings parameter value.')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'payments_gateway_param'
        verbose_name_plural = 'Gateway Params'
        unique_together = ('gateway', 'name')
        
    def __unicode__(self):
        return '%s: %s' % (self.name, self.value)


class Transaction(models.Model):
    """
    Represents a payment transaction
    """
    STATUS_PENDING = 'PE'
    STATUS_PROCESSING = 'PR'
    STATUS_APPROVED = 'AP'
    STATUS_FAILED = 'FA'
    STATUS_REFUNDED = 'RE'
    STATUS_ALL = ((STATUS_PENDING, 'Pending'),
                  (STATUS_PROCESSING, 'Processing'),
                  (STATUS_APPROVED, 'Approved'),
                  (STATUS_FAILED, 'Failed'),
                  (STATUS_REFUNDED, 'Refunded'))

    gateway = models.ForeignKey(Gateway)
    order = models.ForeignKey(Order)
    description = models.CharField(max_length=250)
    error_message = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, choices=STATUS_ALL)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.id)

    def add_param(self, name, value, user):
        """
        Add transaction parameters
        """
        param = TransactionParam(name=name, value=value, created_by=str(user))
        self.params.add(param)
        return param


class TransactionParam(models.Model):
    """
    Represents payment transaction parameters
    """
    transaction = models.ForeignKey(Transaction, related_name='params')
    name = models.CharField(max_length=100, help_text='Transaction parameter name.')
    value = models.CharField(max_length=250, help_text='Transaction parameter value.')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'payments_transaction_param'
        verbose_name_plural = 'Transaction Params'
        unique_together = ('transaction', 'name',)
    
    
    def __unicode__(self):
        return self.name
    
    