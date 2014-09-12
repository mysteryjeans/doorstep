import re
import datetime
import calendar

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from doorsale.payments.models import CardIssuer


class CreditCardForm(forms.Form):
    """
    Credit card payment form
    """
    REGEX_EXPIRY = re.compile(r'^(\d{2})\s/\s(\d{2})$')
    REGEX_CVV2 = re.compile(r'^(\d{3,4})$')

    card_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name...'}), error_messages={'required': 'Please specify name on credit card.'})
    card_number = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Number...'}), error_messages={'required': 'Please specify credit card number.'})
    card_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    expiry = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder': 'MM / YY'}), error_messages={'required': 'Please specify card expiry date'})
    cvv2 = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV2...'}), error_messages={'required': 'Please specify card security code'})

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number'].replace(' ', '')
        try:
            int(card_number)
        except ValueError:
            raise forms.ValidationError("Please specify correct card number.")

        return card_number

    def clean_card_type(self):
        card_type = self.cleaned_data.get('card_type', None)
        card_number = self.cleaned_data.get('card_number', None)

        if card_number and not card_type:
            raise forms.ValidationError('We can\'t recognize your card issuer type.')

        return card_type

    def clean_expiry(self):
        expiry = self.cleaned_data['expiry']
        match = self.REGEX_EXPIRY.search(expiry)

        if match:
            month, year = match.groups()
            try:
                expiry_date = datetime.date(2000 + int(year), int(month), 1)
                if expiry_date > datetime.date.today():
                    return expiry
                else:
                    raise forms.ValidationError("Card expiry date has already been passed.")
            except ValueError:
                pass
        
        raise forms.ValidationError("Please specify correct card expiry date.")

    def clean_cvv2(self):
        cvv2 = self.cleaned_data['cvv2']

        if not self.REGEX_CVV2.search(cvv2):
            raise forms.ValidationError("Please specify correct card security code.")

        return cvv2





