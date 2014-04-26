from django import template
from django.shortcuts import get_object_or_404 

from doorsale.financial.models import Currency


register = template.Library()


@register.filter(name='currency')
def currency(price, currency_code):
    """
    Returns price in currency format
    """
    currency = get_object_or_404(Currency,code=currency_code)
    try:
        return currency.display_format % price
    except Exception:
        raise Exception('Invalid currency format string: "%s" for currency "%s"' % (currency.currency_format, currency.name))