import re
import datetime

from django import forms

from doorstep.payments.models import Gateway


class CreditCardForm(forms.Form):
    """
    Credit card payment form
    """
    REGEX_EXPIRY = re.compile(r'^(\d{2})\s/\s(\d{2})$')
    REGEX_CVV2 = re.compile(r'^(\d{3,4})$')

    gateway = forms.ModelChoiceField(queryset=Gateway.objects.filter(is_active=True, accept_credit_card=True),
                                     empty_label=None, widget=forms.HiddenInput())
    card_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Name...'}),
                                error_messages={'required': 'Please specify name on credit card.'})
    card_number = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'placeholder': 'Number...'}),
                                  error_messages={'required': 'Please specify credit card number.'})
    card_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    expire_date = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder': 'MM / YY'}),
                                  error_messages={'required': 'Please specify card expiry date'})
    cvv2 = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV2...'}),
                           error_messages={'required': 'Please specify card security code'})

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

    def clean_expire_date(self):
        expire_date = self.cleaned_data['expire_date']
        match = self.REGEX_EXPIRY.search(expire_date)

        if match:
            month, year = match.groups()
            try:
                expire_date = datetime.date(2000 + int(year), int(month), 1)
                if expire_date > datetime.date.today():
                    return expire_date
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

    def clean(self):
        cleaned_data = super(CreditCardForm, self).clean()

        if ('card_name' in cleaned_data and 'card_number' in cleaned_data and
                'card_type' in cleaned_data and 'expire_date' in cleaned_data and 'cvv2' in cleaned_data):

            card_name = cleaned_data['card_name']
            expire_date = cleaned_data['expire_date']

            cleaned_data['card'] = {
                'number': cleaned_data['card_number'],
                'type': cleaned_data['card_type'],
                'cvv2': cleaned_data['cvv2'],
                'name': card_name,
                'first_name': card_name.split(' ')[0],
                'last_name': ' '.join(card_name.split(' ')[1:]),
                'expire_month': str(expire_date.month),
                'expire_year': str(expire_date.year)
            }

        return cleaned_data
