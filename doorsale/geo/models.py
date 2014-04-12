from django.db import models


class Country(models.Model):
    """
    Represents a country 
    """
    name = models.CharField(max_length=100, unique=True)
    allow_billing = models.BooleanField(default=True, help_text='Allow billing from this country')
    allow_shipping = models.BooleanField(default=True, help_text='Allow shipping to this country')
    iso_code2 = models.CharField(max_length=2, unique=True, help_text='Two letter ISO code')
    iso_code3 = models.CharField(max_length=3, unique=True, help_text='Three letter ISO code')
    iso_numeric = models.IntegerField(help_text='Numeric ISO code')
    subject_to_vat = models.BooleanField(default=False, help_text='Is VAT applicable')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Countries'
    
    def __unicode__(self):
        return self.name


class State(models.Model):
    """
    Represents a state
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, help_text='Abbrevation')
    country = models.ForeignKey(Country)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
