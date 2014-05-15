from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.core.urlresolvers import reverse

from doorsale.sales.models import Cart
from doorsale.catalog.views import CatalogBaseView
from doorsale.financial.models import Currency        


@transaction.commit_on_success
def add_to_cart(request):   
    """
    Add product to cart
    """
    product_id = int(request.POST['product_id'])
    
    
    # Checking if user already has cart in session
    # otherwise create a new cart for the user    
    if 'cart_id' in request.session:
        cart_id = int(request.session['cart_id'])
        cart = Cart.get_cart(cart_id)
    else:
        cart = Cart.get_cart()
        request.session['cart_id'] = cart.id
    
    try:
        quantity = int(request.POST['quantity'])
        if quantity > 0:
            cart.add_item(product_id, quantity, request.user)
        else:
            raise ValueError()
    except ValueError:
        return HttpResponseBadRequest('Product quantity is not correct, please enter one or more products in numbers.')
    
    if request.is_ajax():
        default_currency = get_default_currency(request)
        return render(request, 'sales/cart_basket.html', {'cart': cart, 'default_currency': default_currency})

    return HttpResponseRedirect(reverse('sales_checkout_cart'))


@transaction.commit_on_success
def remove_from_cart(request):
    """
    Remove product from cart
    """
    product_id = int(request.POST['product_id'])
    
    # Checking if user session has cart or session may already flushed
    # Cart an empty cart for user
    if 'cart_id' in request.session:
        cart_id = int(request.session['cart_id'])
        cart = Cart.get_cart(cart_id)
        cart.remove_item(product_id)
    else:
        cart = Cart()
    
    if request.is_ajax():
        default_currency = get_default_currency(request)
        return render(request, 'sales/cart_basket.html', {'cart': cart, 'default_currency': default_currency})

    return HttpResponseRedirect(reverse('sales_checkout_cart'))


@transaction.commit_on_success
def remove_all_from_cart(request):
    """
    Remove all products from cart
    """
    if request.method == 'POST':
        if 'cart_id' in request.session:
            cart_id = int(request.session['cart_id'])
            cart = Cart.get_cart(cart_id)
            cart.remove_all_items()
        else:
            cart = Cart()
        
        if request.is_ajax():
            default_currency = get_default_currency(request)
            return render(request, 'sales/cart_basket.html', {'cart': cart, 'default_currency': default_currency})

    return HttpResponseRedirect(reverse('sales_checkout_cart'))


class CheckoutBaseView(CatalogBaseView):
    """
    Base checkout steps view
    """
    def get_context_data(self, **kwargs):
        breadcrumbs = self.get_breadcrumbs()
        return super(CheckoutBaseView, self).get_context_data(
            breadcrumbs=breadcrumbs,
            step_active=self.step_active,
            steps_processed=self.steps_processed,
            **kwargs)


class CheckoutCartView(CheckoutBaseView):
    """
    Display user shopping cart
    """
    step_active = 'cart'
    steps_processed = ()
    template_name = 'sales/checkout_cart.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Shopping Cart', 'url': reverse('sales_checkout_cart')},)

    def get(self, request):
        if 'cart_id' in request.session:
            cart_id = int(request.session['cart_id'])
            cart = Cart.get_cart(cart_id)
        else:
            cart = Cart()

        return super(CheckoutCartView, self).get(request, cart=cart)

    def post(self, request):
        error = None
        message = None

        if 'cart_id' in request.session:
            cart_id = int(request.session['cart_id'])
            product_id = int(request.POST['product_id'])
            cart = Cart.get_cart(cart_id)
            try:
                quantity = int(request.POST['quantity'])
                if quantity > 0:
                    cart.update_item(product_id, quantity)
                    message = 'Your shopping cart has been updated.'
                else:
                    raise ValueError()
            except ValueError:
                error = 'Product quantity is not correct, please enter one or more products in numbers.'
            
        else:
            cart = Cart()

        return super(CheckoutCartView, self).get(request, cart=cart, error=error, message=message)


class CheckoutBillingView(CheckoutBaseView):
    """
    Display user billing address
    """
    step_active = 'billing'
    steps_processed = ['cart']
    template_name = 'sales/checkout_billing.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Billing Address', 'url': reverse('sales_checkout_billing')},)


class CheckoutShippingView(CheckoutBaseView):
    """
    Display user shipping address
    """
    step_active = 'shipping'
    steps_processed = ['cart', 'address']
    template_name = 'sales/checkout_shipping.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Address', 'url': reverse('sales_checkout_shipping')},)


class CheckoutPaymentView(CheckoutBaseView):
    """
    Display payment method for checkout
    """
    step_active = 'payment'
    steps_processed = ['cart', 'address', 'shipping']
    template_name = 'sales/checkout_payment.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Payment', 'url': reverse('sales_checkout_payment')},)


class CheckoutOrderView(CheckoutBaseView):
    """
    Display user order information
    """
    step_active = 'order'
    steps_processed = ['cart', 'address', 'shipping', 'payment']
    template_name = 'sales/checkout_order.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Order', 'url': reverse('sales_checkout_order')},)


class CheckoutReceiptView(CheckoutBaseView):
    """
    Display user order receipt
    """
    step_active = 'receipt'
    steps_processed = []
    template_name = 'sales/checkout_receipt.html'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Order Receipt', 'url': reverse('sales_checkout_receipt')},)


def get_default_currency(request):
    if 'default_currency' in request.session:
        try:
            return Currency.objects.get(code=request.session['default_currency']) 
        except Currency.DoesNotExist:
            return Currency.get_primary()
    
    return Currency.get_primary()


