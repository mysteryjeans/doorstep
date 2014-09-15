from django.db import transaction
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from doorsale.exceptions import DoorsaleError
from doorsale.sales.models import Order
from doorsale.catalog.views import get_default_currency
from doorsale.payments.forms import CreditCardForm
from doorsale.payments.models import Gateway
from doorsale.payments.processors import PayPal, Stripe


def online_payment(request, order_id, receipt_code):   
    """
    Shows online or process online payment
    """
    order = get_object_or_404(Order, id=order_id, receipt_code=receipt_code)
    default_currency = get_default_currency(request)

    form = None
    gateways = Gateway.get_gateways()
    for gateway in gateways:
        if gateway.accept_credit_card:
            form = CreditCardForm(initial={ 'gateway': gateway })
    return render(request, 'payments/online_payment.html', { 'form': form, 'order': order, 'gateways': gateways, 'default_currency': default_currency })


@transaction.non_atomic_requests
def credit_card_payment(request, order_id, receipt_code):
    """
    Process credit card payment
    """
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        order = get_object_or_404(Order, id=order_id, receipt_code=receipt_code)
        
        if form.is_valid():
            error = None
            data = form.cleaned_data
            gateway = data['gateway']
            
            if gateway.name == Gateway.PAYPAL:
                processor = PayPal(gateway)
            elif gateway.name == Gateway.STRIPE:
                processor = Stripe(gateway)
            else:
                raise ImproperlyConfigured('%s is not supported gateway for processing credit cards.' % gateway)

            try:
                transaction = processor.credit_card_payment(data['card'], order, request.user)
                return render(request, 'payments/credit_card_processed.html', { 'order': order })
            except DoorsaleError as e:
                error = e.message
     
        gateways = Gateway.get_gateways()
        default_currency = get_default_currency(request)
        return render(request, 'payments/online_payment.html', { 'form': form, 'order': order, 'gateways': gateways, 'default_currency': default_currency, 'error': error })

    raise Http404


@transaction.non_atomic_requests
def account_payment(request, order_id, receipt_code):
    """
    Process payment via online account like PayPal, Amazon ...etc
    """
    order = get_object_or_404(Order,id=order_id, receipt_code=receipt_code)
    if request.method == "POST":
        gateway_name = request.POST["gateway_name"]
        gateway = get_object_or_404(Gateway, name=gateway_name)

        raise ImproperlyConfigured('Doorsale doesn''t yet support Payment Processing Gateway: "%s"' % gateway.get_name_display())

    raise Http404
