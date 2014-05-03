from django import template
from django.conf import settings

from doorsale.sales.models import Cart


register = template.Library()


@register.inclusion_tag('sales/cart_basket.html', takes_context=True)
def cart_basket(context):
    """
    Returns cart summary
    """
    request = context['request']
    default_currency = context['default_currency']
    
    if 'cart_id' in request.session:
        cart = Cart.get_cart(int(request.session['cart_id']))
    else:
        cart = Cart()
    
    return {'cart': cart, 'default_currency': default_currency, 'MEDIA_URL': settings.MEDIA_URL }