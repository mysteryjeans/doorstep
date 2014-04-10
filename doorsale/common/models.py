from django.db import models
from django.contrib.auth.models import AbstractUser


class Country(models.Model):
    """
    Represents a country 
    """
    name = models.CharField(max_length=100, unique=True)
    allow_billing = models.BooleanField(default=True, help_text='Allow billing from this country')
    allow_shipping = models.BooleanField(default=True, help_text='Allow shipping to this country')
    iso_code2 = models.CharField(max_length=2, unique=True, help_text='Two letter ISO code')
    iso_code3 = models.CharField(max_length=3, unique=True, help_text='Three letter ISO code')
    iso_numerice = models.IntegerField(help_text='Numeric ISO code')
    subject_to_vat = models.BooleanField(default=False, help_text='Is VAT applicable')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name 
    

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
