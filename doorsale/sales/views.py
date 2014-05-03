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
    default_currency = get_default_currency(request)
    
    # Checking if user already has cart in session
    # otherwise create a new cart for the user    
    if 'cart_id' in request.session:
        cart_id = int(request.session['cart_id'])
        cart = Cart.get_cart(cart_id)
    else:
        cart = Cart.get_cart()
        request.session['cart_id'] = cart.id
    
    cart.add_item(product_id, quantity, request.user)
    
    return render(request, 'sales/cart_basket.html', {'cart': cart, 'default_currency': default_currency})


@transaction.commit_on_success
def remove_from_cart(request):
    """
    Remove product from cart
    """
    product_id = int(request.POST['product_id'])
    default_currency = get_default_currency(request)
    
    # Checking if user session has cart or session may already flushed
    # Cart an empty cart for user
    if 'cart_id' in request.session:
        cart_id = int(request.session['cart_id'])
        cart = Cart.get_cart(cart_id)
        cart.remove_item(product_id)
    else:
        cart = Cart()
    
    return render(request, 'sales/cart_basket.html', {'cart': cart, 'default_currency': default_currency})


def get_default_currency(request):
    if 'default_currency' in request.session:
        try:
            return Currency.objects.get(code=request.session['default_currency']) 
        except Currency.DoesNotExist:
            return Currency.get_primary()
    
    return Currency.get_primary()


