from django.db import transaction
from django.shortcuts import render

from doorsale.sales.models import Cart
from doorsale.financial.models import Currency        


@transaction.commit_on_success
def add_to_cart(request):   
    """
    Add product to cart
    """
    product_id = int(request.POST['product_id'])
    quantity = int(request.POST['quantity'])
    
    if 'cart_id' in request.session:
        cart = Cart.get_cart(int(request.session['cart_id']))
    else:
        cart = Cart.get_cart()
        request.session['cart_id'] = cart.id
    
    cart.add_item(product_id, quantity, request.user)
    
    if 'default_currency' in request.session:
        try:
            default_currency = Currency.objects.get(code=request.session['default_currency']) 
        except Currency.DoesNotExist:
            default_currency = Currency.get_primary()
    
    return render(request, 'sales/cart_summary.html', {'cart': cart, 'default_currency': default_currency})
        