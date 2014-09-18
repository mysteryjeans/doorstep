from django import forms

from doorsale.geo.models import State, Address


class AddressForm(forms.ModelForm):
    """
    Address form for checkout
    """
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'email', 'address1', 'address2',
                  'phone_number', 'fax_number', 'zip_or_postal_code', 'city', 'country', 'state', 'company')
        widgets = {
            'first_name': forms.TextInput(attrs=({'placeholder': 'First name...', 'class': 'mandatory'})),
            'last_name': forms.TextInput(attrs=({'placeholder': 'Last name...', 'class': 'mandatory'})),
            'email': forms.TextInput(attrs=({'placeholder': 'Email address...', 'class': 'mandatory'})),
            'phone_number': forms.TextInput(attrs=({'placeholder': 'Phone number...', 'class': 'mandatory'})),
            'fax_number': forms.TextInput(attrs=({'placeholder': 'Fax number... (Optional)', 'class': 'optional'})),
            'address1': forms.TextInput(attrs=({'placeholder': 'Address line 1...', 'class': 'mandatory'})),
            'address2': forms.TextInput(attrs=({'placeholder': 'Address line 2... (Optional)', 'class': 'optional'})),
            'zip_or_postal_code': forms.TextInput(attrs=({'placeholder': 'Zip/Postal Code...', 'class': 'mandatory'})),
            'city': forms.TextInput(attrs=({'placeholder': 'City...', 'class': 'mandatory'})),
            'Country': forms.Select(attrs=({'placeholder': 'Country...', 'class': 'mandatory'})),
            'company': forms.TextInput(attrs=({'placeholder': 'Company... (Optional)', 'class': 'optional'})),

        }
        error_messages = {
            'first_name': {'required': 'Please enter your first name.'},
            'last_name': {'required': 'Please enter your last name.'},
            'email': {'required': 'Please enter your email address.'},
            'address1': {'required': 'Please enter your address.'},
            'city': {'required': 'Please specify your city.'},
            'zip_or_postal_code': {'required': 'Please enter Zip or Postal Code.'},
            'country': {'required': 'Please specify your country.'},
            'phone_number': {'required': 'Please entery your phone number.'}
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = None

    @classmethod
    def get_states(cls):
        return list(State.objects.filter(is_active=True).all())
