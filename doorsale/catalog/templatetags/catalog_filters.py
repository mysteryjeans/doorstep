import locale 

from django import template 
from django.core.exceptions import ImproperlyConfigured

register = template.Library()
locale.setlocale(locale.LC_ALL, 'en_US')

@register.filter(name='currency')
def currency(price, currency):
    """
    Returns price in currency format
    """
    price = float(price) * currency.exchange_rate
    try:
        print currency.display_format
        return currency.display_format.format(price)
    except Exception as e:
        raise ImproperlyConfigured('Invalid currency format string: "%s" for currency "%s". ' % (currency.display_format, currency.name)
                                   + e.message )