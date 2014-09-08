import datetime
import calendar

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from doorsale.payments.models import CardIssuer


this_year = datetime.datetime.today().year

MONTHS = list((i, calendar.month_name[i]) for i in range(1, 13))
YEARS = list((i, i) for i in range(this_year, this_year + 10))


class CreditCardForm(forms.Form):
    """
    Credit card payment form
    """
    card_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name'}), error_messages={'required': 'Please enter name on credit card.'})
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'placeholder': 'Card number'}), error_messages={'required': 'Please enter credit card number.'})
    card_type = forms.ModelChoiceField(queryset=CardIssuer.objects.filter(is_active=True), empty_label='Type')
    cvv2 = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV2'}))
    expire_month = forms.ChoiceField(choices=MONTHS)
    expire_year = forms.ChoiceField(choices=YEARS)

