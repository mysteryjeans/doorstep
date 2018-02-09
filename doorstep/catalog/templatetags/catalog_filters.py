from django import template 
from django.core.exceptions import ImproperlyConfigured


register = template.Library()


@register.filter(name='currency')
def currency(price, currency):
    """
    Returns price in currency format
    """
    price = float(price)
    price *= float(currency.exchange_rate)
    try:
        return currency.display_format.format(price)
    except Exception as e:
        raise ImproperlyConfigured('Invalid currency format string: "%s" for currency "%s". %s' % (currency.display_format, currency.name, e.message))