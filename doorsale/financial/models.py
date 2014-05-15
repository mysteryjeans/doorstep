from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured

class Currency(models.Model):
    """
    Represents a currency
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="ISO Currency Code")
    exchange_rate = models.FloatField(default=1.0)
    locale = models.CharField(max_length=10, blank=True)
    display_format = models.CharField(max_length=50, help_text='Display format: 1.2 => "${0:,.2f}".format(price) => $1.20 (python format string)')
    is_primary = models.BooleanField(default=False,
                                     help_text='Default currency of prices & costs. When you change primary currency, make sure to update exchange rates, prices & costs.')
    is_active = models.BooleanField(default=False)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Currencies'
    
    def __unicode__(self):
        return self.name
    
    def clean(self):
        if self.is_primary:
            
            if not self.is_active:
                raise ValidationError('Cannot inactive primary currency.')
            
            if self.exchange_rate != 1:
                raise ValidationError('Primary should have exchange rate of 1. '
                                      'All prices & cost should be defined in primary currency value.')
        
            try:
                primary_currency = type(self).objects.get(is_primary=True)
                if self.id != primary_currency.id:
                    raise ValidationError('"%s" is already defined as primary currency.' % unicode(primary_currency))
            except type(self).DoesNotExist:
                pass
    
    @classmethod
    def get_primary(cls):
        """
        Returns primary currency
        """
        try:
            return cls.objects.get(is_active=True, is_primary=True)
        except cls.DoesNotExist:
            raise ImproperlyConfigured('Primary currency not defined in the system.')
    
    @classmethod
    def get_currencies(cls):
        return list(cls.objects.filter(is_active=True))


class TaxRate(models.Model):
    """
    Represents a Tax Category
    """
    TAX_PERCENTAGE = 'PE'
    TAX_FIXED = 'FI'
    TAX_METHODS = ((TAX_PERCENTAGE, 'Percentage'),
                   (TAX_FIXED, 'Fixed'))
    
    name = models.CharField(max_length=100, unique=True)
    method = models.CharField(max_length=2, choices=TAX_METHODS, help_text='Tax deduction method: fixed tax per product or percentage (in fraction) of price per product')
    rate = models.FloatField(default=0.0)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'financial_tax_rate'
        verbose_name_plural = 'Tax Rates'
    
    def __unicode__(self):
        return '%s [%s]: %s' % (self.name, self.method, self.rate)
    
    def calculate(self, price, quantity):
        """
        Calculate tax on price & quantity based on tax method
        """
        return self._calculate(price, quantity, self.method, self.rate, self.name) 
    
    @classmethod
    def get_taxes(cls):
        """
        Return all taxes defined in system
        """
        return list(cls.objects.all())
    
    @classmethod
    def _calculate(cls, price, quantity, method, rate, name=None):
        """
        Calculate tax on price & quantity based on tax method
        """
        if method == cls.TAX_FIXED:
            return float(rate) * float(quantity)
        elif method == cls.TAX_PERCENTAGE:
            return float(rate) * float(quantity) * float(price)
        
        if name:
            raise Exception('Unknown tax method "%s" defined for tax rate: "%s"' % (method, name))
        
        raise Exception('Unknown tax method "%s"' % method)  
