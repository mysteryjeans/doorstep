from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.http.response import Http404
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404

from doorsale.geo.models import Address
from doorsale.sales.models import Cart, Order, PaymentMethod
from doorsale.sales.forms import AddressForm
from doorsale.catalog.views import CatalogBaseView
from doorsale.financial.models import Currency
from doorsale.exceptions import DoorsaleError
from doorsale.views import BaseView
from doorsale.utils.helpers import send_mail



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


class CheckoutAddressView(CheckoutBaseView):
    """
    Base checkout view for billing and shipping address
    """
    template_name = 'sales/checkout_address.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutAddressView, self).get_context_data(**kwargs)
        
        addresses_filter = None
        request = self.request

        if request.user.is_authenticated():
            addresses_filter = Q(email__iexact=request.user.email) | Q(customer=request.user)
            
        if 'addresses' in request.session:
            addresses_ids = request.session['addresses']
            addresses_filter = addresses_filter | Q(id__in=addresses_ids) if addresses_filter else Q(id__in=addresses_ids)
        
        if addresses_filter:
            context['addresses'] = list(Address.objects.filter(addresses_filter))

        context['current_step'] = self.current_step

        return context

    def get(self, request, **kwargs):
        form = AddressForm()

        if self.session_address_key in request.session:
            del request.session[self.session_address_key]

        return super(CheckoutAddressView, self).get(request, form=form, **kwargs)

    def post(self, request):
        form = AddressForm(request.POST)
        address_id = request.POST['address_id']

        if address_id:
            address_id = int(address_id)
            address = get_object_or_404(Address, id=address_id)

            # Binding address permenantly to authenticated user
            if address.customer is None and request.user.is_authenticated():
                address.customer = request.user
                address.save()

            request.session[self.session_address_key] = address_id
            return HttpResponseRedirect(reverse(self.next_step))

        if form.is_valid():
            data = form.cleaned_data
            customer = request.user if request.user.is_authenticated() else None

            address = Address.objects.create(
                customer=customer,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                address1=data['address1'],
                address2=data['address2'],
                phone_number=data['phone_number'],
                fax_number=data['fax_number'],
                zip_or_postal_code=data['zip_or_postal_code'],
                city=data['city'],
                country=data['country'],
                state=data['state'],
                company=data['company'],
                created_by=str(request.user),
                updated_by=str(request.user))

            addresses = self.request.session.get('addresses', [])
            addresses.append(address.id)
            self.request.session['addresses'] = addresses
            request.session[self.session_address_key] = address.id

            return HttpResponseRedirect(reverse(self.next_step))

        return super(CheckoutAddressView, self).get(request, form=form)


class CheckoutBillingView(CheckoutAddressView):
    """
    User billing address for order
    """
    step_active = 'billing'
    steps_processed = ['cart']
    current_step = 'sales_checkout_billing'
    next_step = 'sales_checkout_shipping'
    session_address_key = 'billing_address'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Billing Address', 'url': reverse('sales_checkout_billing')},)


class CheckoutShippingView(CheckoutAddressView):
    """
    Display user shipping address
    """
    step_active = 'shipping'
    steps_processed = ['cart', 'billing']
    current_step = 'sales_checkout_shipping'
    next_step = 'sales_checkout_payment'
    session_address_key = 'shipping_address'

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Shipping Address', 'url': reverse('sales_checkout_shipping')},)


class CheckoutPaymentView(CheckoutBaseView):
    """
    Display payment method for checkout
    """
    step_active = 'payment'
    steps_processed = ['cart', 'billing', 'shipping']
    template_name = 'sales/checkout_payment.html'
    
    def get_context_data(self, **kwargs):
        payment_methods = PaymentMethod.get_all()
        return super(CheckoutPaymentView, self).get_context_data(payment_methods=payment_methods, **kwargs)

    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Payment', 'url': reverse('sales_checkout_payment')},)
    
    def get(self, request):
        po_number = request.session.get('po_number', None)
        payment_method = request.session.get('payment_method', None)
        
        return super(CheckoutPaymentView, self).get(request, payment_method=payment_method, po_number=po_number)
    
    def post(self, request):
        error = None
        payment_method = request.POST.get('payment_method', None)
        payment_methods = dict(PaymentMethod.ALL)
        if payment_method and payment_method in payment_methods:
            
            if payment_method == PaymentMethod.PURCHASE_ORDER:
                po_number = request.POST['po_number']
                if po_number:
                    request.session['po_number'] = po_number
                    request.session['payment_method'] = payment_method
                    return HttpResponseRedirect(reverse('sales_checkout_order'))
                else:
                    error = 'Please provide purchase order number.'
            else:
                if 'po_number' in request.session:
                    del request.session['po_number']
                    
                request.session['payment_method'] = payment_method
                return HttpResponseRedirect(reverse('sales_checkout_order'))
        else:
            error = 'Please select payment method'
        
        return super(CheckoutPaymentView, self).get(request, error=error, payment_method=payment_method)


class CheckoutOrderView(CheckoutBaseView):
    """
    Display user order information
    """
    step_active = 'order'
    steps_processed = ['cart', 'billing', 'shipping', 'payment']
    template_name = 'sales/checkout_order.html'
    decorators = [transaction.commit_on_success]
    
    @classmethod
    def get_breadcrumbs(cls):
        return ({'name': 'Order', 'url': reverse('sales_checkout_order')},)
    
    def get(self, request, **kwargs):
        if ('cart_id' in request.session
            and 'payment_method' in request.session
            and CheckoutBillingView.session_address_key in request.session
            and CheckoutShippingView.session_address_key in request.session):
            
            cart = Cart.get_cart(int(request.session['cart_id']))
            payment_method = PaymentMethod.ALL_METHODS[request.session['payment_method']]
            billing_address = get_object_or_404(Address, id=int(request.session[CheckoutBillingView.session_address_key]))
            shipping_address = get_object_or_404(Address, id=int(request.session[CheckoutShippingView.session_address_key]))
            
            return super(CheckoutOrderView, self).get(request, cart=cart, payment_method=payment_method, billing_address=billing_address, shipping_address=shipping_address, **kwargs)
        
        return HttpResponseRedirect(reverse('sales_checkout_cart'))
    
    def post(self, request):
        error = None
        try:
            cart_id = request.session['cart_id']
            payment_method = request.session['payment_method']
            po_number = request.session.get('po_number', None)
            billing_address_id = request.session[CheckoutBillingView.session_address_key]
            shipping_address_id = request.session[CheckoutShippingView.session_address_key]
            
            if payment_method == PaymentMethod.CREDIT_CARD:
                raise DoorsaleError('Payment method not supported: %s' % PaymentMethod.ALL_METHODS[payment_method])
            
            if request.user.is_authenticated():
                user = request.user
                username = str(user)
            else:
                user = None
                username = str(request.user)
                
            currency_code = self.request.session.get('default_currency', self.primary_currency.code)
            order = Order.objects.place(cart_id, billing_address_id, shipping_address_id, payment_method, po_number, currency_code, user, username)
            
            del request.session['cart_id']
            del request.session['payment_method']
            del request.session['billing_address']
            del request.session['shipping_address']
            request.session['order_confirmed'] = True
            
            # Sending order confirmation email to user's billing email address
            msg_subject = get_template("sales/email/order_confirmation_subject.txt").render(Context({'order': order, 'user': request.user, 'SITE_NAME': settings.SITE_NAME, 'DOMAIN': settings.DOMAIN }))
            msg_text = get_template("sales/email/order_confirmation.html").render(Context({'order': order, 'user': request.user, 'SITE_NAME': settings.SITE_NAME, 'DOMAIN': settings.DOMAIN  }))
            to_email = '%s <%s>' % (order.billing_address.get_name(), order.billing_address.email)
            send_mail(msg_subject, msg_text, [to_email], True)
            
            return HttpResponseRedirect(reverse('sales_checkout_receipt', args=[order.id, order.receipt_code]))
            
        except DoorsaleError as e:
            error = e.message
        
        return self.get(request, error=error)


class CheckoutReceiptView(CheckoutBaseView):
    """
    Display user order receipt
    """
    step_active = 'receipt'
    steps_processed = []
    template_name = 'sales/checkout_receipt.html'

    def get_breadcrumbs(self):
        return ({'name': 'Order Receipt', 'url': reverse('sales_checkout_receipt', args=[self.order_id, self.receipt_code])},)
    
    def get(self, request, order_id, receipt_code):
        order_id = int(order_id)
        order_confirmed = request.session.pop('order_confirmed', None)
            
        try:
            order = Order.objects.prefetch_related('billing_address', 'shipping_address', 'payment_method', 'currency', 'items').get(id=order_id, receipt_code=receipt_code)
        except Order.DoesNotExist:
            raise Http404()
        
        self.order_id = order_id
        self.receipt_code = receipt_code
        
        return super(CheckoutReceiptView, self).get(request, order=order, order_confirmed=order_confirmed)


class PrintReceiptView(BaseView):
    """
    Print user order receipt
    """
    template_name = 'sales/print_receipt.html'

    def get(self, request, order_id, receipt_code):
        order_id = int(order_id)
        try:
            order = Order.objects.prefetch_related('billing_address', 'shipping_address', 'payment_method', 'currency', 'items').get(id=order_id, receipt_code=receipt_code)
        except Order.DoesNotExist:
                raise Http404()
    
        return super(PrintReceiptView, self).get(request, order=order)


def get_default_currency(request):
    if 'default_currency' in request.session:
        try:
            return Currency.objects.get(code=request.session['default_currency']) 
        except Currency.DoesNotExist:
            return Currency.get_primary()
    
    return Currency.get_primary()


