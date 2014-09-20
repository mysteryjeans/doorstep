from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import ImproperlyConfigured


def send_mail(subject, message, recipients, is_html):
    if not hasattr(settings, 'SITE_NAME') or not hasattr(settings, 'DOMAIN'):
        raise ImproperlyConfigured('SITE_NAME and DOMAIN not found in django settings.')

    if not hasattr(settings, 'EMAIL_HOST') or not hasattr(settings, 'EMAIL_PORT'):
        raise ImproperlyConfigured('Email configurations not found in django settings.')

    from_email = '%s <noreply@%s>' % (settings.SITE_NAME, settings.DOMAIN)
    msg = EmailMessage(subject, message, from_email, recipients)
    if is_html:
        msg.content_subtype = "html"
    msg.send()
