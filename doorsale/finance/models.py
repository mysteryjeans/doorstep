from django.db import models

class Currency(models.Model):
    """
    Represents a currency
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="ISO Currency Code")
    is_active = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False, help_text='Primary currency of site, you should updated exchange rate and product prices when you choose change primary currency')
    exchange_rate = models.FloatField(default=1.0)
    price_format = models.CharField(max_length=100, help_text='Price format: "${price}"')
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    

class TaxCategory(models.Model):
    """
    Represents a Tax Category
    """
    category = models.ForeignKey('catalog.Category')
    tax_rate = models.FloatField(default=0.0)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'finance_tax_category'
        verbose_name_plural = 'Tax Categories'
    
    def __unicode__(self):
        return '%s: %s' % (self.category, self.tax_rate)
