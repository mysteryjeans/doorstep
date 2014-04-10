from django.db import models
from django.contrib.auth.models import AbstractUser

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
