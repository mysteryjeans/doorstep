from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import ImproperlyConfigured

from doorsale.models import SysConfig


def send_mail(subject, message, recipients, is_html):
    """
    Sends email using predefined System Configs and Django settings
    """
    sys_configs = SysConfig.get_configs()

    if 'SITE_NAME' not in sys_configs or 'DOMAIN' not in sys_configs:
        raise ImproperlyConfigured('SITE_NAME and DOMAIN not found. It should be defined in System Configurations')

    if not hasattr(settings, 'EMAIL_HOST') or not hasattr(settings, 'EMAIL_PORT'):
        raise ImproperlyConfigured('Email server configurations not found in django settings.py.')

    from_email = '%s <noreply@%s>' % (sys_configs['SITE_NAME'], sys_configs['DOMAIN'])
    msg = EmailMessage(subject, message, from_email, recipients)
    if is_html:
        msg.content_subtype = "html"
    msg.send()
