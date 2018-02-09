.. _ref-config:

=============
Configuration
=============

Doorstep also requires settings to be defined in ``settings.py``, you have
probably :doc:`create new project <project>` for site which should have following
extra settings beside standard Django settings parameters:

.. code-block:: python

    ################## Doorstep #########################
    # Doorstep e-commerce settings for Django project
    # Customize these settings only if you know
    from doorstep.settings import *
    INSTALLED_APPS += DOORSALE_APPS

This code is effectively importing all the settings required by Doorstep into
your project's ``settings.py``. However Doorstep apps doesn't replace your
project's ``INSTALLED_APPS``, therefore ``DOORSALE_APPS`` must be added to
your projects installed apps explicitly.


.. admonition:: Override Settings!

    All settings variable should be defined after Doorstep's default imported in
    ``settings.py``

User Model
==========

Doorstep extends ``django.contrib.auth`` by driving from Django's `auth user model`_
abstract classes and defined it's own user auth model in ``settings.py``.
Where ``accounts.User`` is compose of app name **accounts** that contains auth user model **User**. ::

    AUTH_USER_MODEL = 'accounts.User'

You can extend Doorstep's auth user model in similar way by creating your own
authentication app ``myauth`` and drive ``MyUser`` user model from abstract
classes provided in ``doorstep.accounts``. ::

    from django.db import models
    from doorstep.accounts.models import AbstractUser

    class MyUser(AbstractUser):
        mail_digest = models.BooleanField(default=True)

Lastly override ``AUTH_USER_MODEL`` in project ``settings.py`` after Doorstep settings.
Remember to use ``get_user_model`` from ``django.contrib.auth`` instead of
directly references user auth model class. ::

    AUTH_USER_MODEL = 'myauth.MyUser'

.. _auth user model: https://docs.djangoproject.com/en/stable/ref/contrib/auth/


Login Auth
==========

Authenticate is handle by accounts apps, you don't need to override login url
for your custom ``AUTH_USER_MODEL``. If you want to implement your custom login
page, let say for integration with other account services like Google & Facebook.
You can simple implement your custom login and override login url to hit your own View ::

    LOGIN_URL = '/accounts/login/'


Login Redirect
==============

After authentication if return URL is exists in ``next`` parameter in query string
then user will automatically redirect URL defined login redirect url ::

    LOGIN_REDIRECT_URL = '/'
