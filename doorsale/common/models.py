from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from ..geo.models import Country, State


class Address(models.Model):
    """
    Represents a address for billing and shipping
    """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    country = models.ForeignKey(Country, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    city = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    zip_or_postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Addresses'
    
    def __unicode__(self):
        address = '%s %s %s' % (self.first_name, self.last_name, self.address1)
        
        if self.address2:
            address += ' ' + self.address2
        
        address += ', ' + self.city
        
        if self.state:
            address += ', ' + unicode(self.state)
        
        if self.country:
            address += ', ' + unicode(self.country)
        
        return address


class BaseUser(AbstractUser):
    """
    An abstract class extending Django auth user model for doorsale.
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = ((MALE, 'Male'),
               (FEMALE, 'Female'))
    
    birthday = models.DateField(null=True, blank=True)    
    gender = models.CharField(max_length=1, choices=GENDERS)
    billing_address = models.ForeignKey(Address, null=True, blank=True, related_name='billing_customers', help_text='Customer default billing address')
    shipping_adress = models.ForeignKey(Address, null=True, blank=True, related_name='shipping_customers', help_text='Customer default shipping address')
    is_verified = models.BooleanField(default=False)    
    verification_code = models.CharField(max_length=512, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    
    REQUIRED_FIELDS = ['email', 'is_verified', 'updated_by', 'created_by']
    
    class Meta:
        abstract = True


class User(BaseUser):
    """
    Extends Django auth user model for doorsale.
    """


        