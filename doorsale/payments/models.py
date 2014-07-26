from __future__ import unicode_literals

from django.db import models

from doorsale.sales.models import Order
 

class Gateway(models.Model):
    """
    Represents payment processing gateways
    """
    PAYPAL = 'PP'
    AMAZON_PAYMENTS = 'AP'
    ALL = ((PAYPAL, 'PayPal'),
           (AMAZON_PAYMENTS, 'Amazon Payments'))
    
    name = models.CharField(primary_key=True, max_length=10, choices=ALL, help_text='Payment processing gateway.')
    account_name = models.CharField(max_length=100, help_text='Payment account name, usually it is your configured business email address of your merchant account.')
    is_active = models.BooleanField(help_text='Gateway active for customer to buy through it.')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s %s' % (self.account_name, self.type)


class GatewayParam(models.Model):
    """
    Represents a payment processing gateway settings
    """
    gateway = models.ForeignKey(Gateway)
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
        
    def __unique__(self):
        return '%s: %s' % (self.name, self.value)


class Transaction(models.Model):
    """
    Represents a payment transaction
    """
    gateway = models.ForeignKey(Gateway)
    order = models.ForeignKey(Order)
    stan = models.CharField(max_length=100,
                            help_text='External system transaction id, this should be unique by gateway.')
    sale_id = models.CharField(max_length=100, null=True, blank=True,
                               help_text='External system sale id, if any.')
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    refund_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return unicode(self.id)


class TransactionParam(models.Model):
    """
    Represents payment transaction parameters
    """
    transaction = models.ForeignKey(Transaction)
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
    
    