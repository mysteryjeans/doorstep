from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser as _AbstractUser, UserManager as _UserManager

from doorsale.geo.models import Address
from doorsale.utils.helpers import random_digest


class UserManager(_UserManager):

    def register(self, first_name, last_name, email, gender, username, password, is_verified=False, **extra_fields):
        """
        Creates a new user in database, and also marked first user as staff and superuser
        """
        # Is verified can be later use to verify user email address
        verification_code = None
        if not is_verified:
            verification_code = random_digest()

        if self.filter(email__iexact=email).count() > 0:
            raise ValidationError("User with this Email address already exists.")

        # First user will automatically become super user and staff member
        if self.count() == 0:
            user = self.create_superuser(username=username,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         password=password,
                                         gender=gender,
                                         is_verified=is_verified,
                                         verification_code=verification_code,
                                         updated_by=username,
                                         created_by=username,
                                         **extra_fields)
        else:
            user = self.create_user(username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password,
                                    gender=gender,
                                    is_verified=is_verified,
                                    verification_code=verification_code,
                                    updated_by=username,
                                    created_by=username,
                                    **extra_fields)

        return user


class AbstractUser(_AbstractUser):

    """
    An abstract class extending Django authentication user model for Doorsale.
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = ((MALE, 'Male'),
               (FEMALE, 'Female'))

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default=None)
    billing_address = models.ForeignKey(Address, null=True, blank=True, related_name='billing_customers',
                                        help_text='Customer default billing address')
    shipping_adress = models.ForeignKey(Address, null=True, blank=True, related_name='shipping_customers',
                                        help_text='Customer default shipping address')
    is_verified = models.BooleanField(default=True)
    verification_code = models.CharField(max_length=512, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'gender', 'updated_by', 'created_by']

    class Meta:
        abstract = True

    @classmethod
    def get_by_username(cls, username):
        """
        Returns user for specified username or raised DoesNotExist exception
        """
        return cls.objects.get(username__iexact=username)


class User(AbstractUser):

    """
    Extends Django authentication user model for Doorsale.
    """
