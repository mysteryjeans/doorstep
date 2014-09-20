from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser as _AbstractUser, UserManager as _UserManager

from doorsale.exceptions import DoorsaleError
from doorsale.geo.models import Address


class UserManager(_UserManager):

    def register(self, first_name, last_name, email, gender, username, password, is_verified=False, **extra_fields):
        """
        Creates a new user in database, and also marked first user as staff and superuser
        """
        # Is verified can be later use to verify user email address
        verify_code = None
        if not is_verified:
            verify_code = self.make_random_password(length=20)

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
                                         verify_code=verify_code,
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
                                    verify_code=verify_code,
                                    updated_by=username,
                                    created_by=username,
                                    **extra_fields)

        return user

    def get_reset_code(self, email):
        """
        Generates a new password reset code returns user
        """

        try:
            user = self.get(email__iexact=email)
            user.reset_code = self.make_random_password(length=20)
            user.reset_code_expire = timezone.now() + timedelta(days=2)
            user.save()

            return user
        except get_user_model().DoesNotExist:
            raise DoorsaleError('We can\'t find that email address, sorry!')

    def reset_password(self, user_id, reset_code, password):
        """
        Set new password for the user
        """

        if not password:
            raise DoorsaleError('New password can\'t be blank.')

        try:
            user = self.get(id=user_id)
            if not user.reset_code or user.reset_code != reset_code or user.reset_code_expire < timezone.now():
                raise DoorsaleError('Password reset code is invalid or expired.')

            # Password reset code shouldn't be used again
            user.reset_code = None
            user.set_password(password)
            user.save()

        except get_user_model().DoesNotExist:
            raise DoorsaleError('Password reset code is invalid or expired.')

    def change_password(self, user, current_password, password):
        """
        Updates user's current password
        """

        if not password:
            raise DoorsaleError('New password can\'t be blank.')

        # Changing user's password if old password verifies
        user = self.get(id=user.id)

        if not user.check_password(current_password):
            raise DoorsaleError('Your current password is wrong.')

        user.set_password(password)
        user.save()


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
    verify_code = models.CharField(max_length=512, blank=True, null=True,
                                   help_text='User account verification code.', editable=False)
    reset_code = models.CharField(max_length=512, blank=True, null=True,
                                  help_text='Password reset code.', editable=False)
    reset_code_expire = models.DateTimeField(max_length=512, blank=True, null=True,
                                             help_text='Password reset code expire date.', editable=False)
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
