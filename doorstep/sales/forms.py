from django import forms

from doorstep.geo.models import Country, State, Address


class AddressForm(forms.ModelForm):
    """
    Address form for checkout
    """
    class Meta:
        model = Address
        fields = ('first_name', 'last_name', 'email', 'address1', 'address2',
                  'phone_number', 'fax_number', 'zip_or_postal_code', 'city', 'country', 'state', 'company')
        widgets = {
            'first_name': forms.TextInput(attrs=({'placeholder': 'First name...'})),
            'last_name': forms.TextInput(attrs=({'placeholder': 'Last name...'})),
            'email': forms.TextInput(attrs=({'placeholder': 'Email address...'})),
            'phone_number': forms.TextInput(attrs=({'placeholder': 'Phone number...'})),
            'fax_number': forms.TextInput(attrs=({'placeholder': 'Fax number... (Optional)'})),
            'address1': forms.TextInput(attrs=({'placeholder': 'Address line 1...'})),
            'address2': forms.TextInput(attrs=({'placeholder': 'Address line 2... (Optional)'})),
            'zip_or_postal_code': forms.TextInput(attrs=({'placeholder': 'Zip/Postal Code...'})),
            'city': forms.TextInput(attrs=({'placeholder': 'City...'})),
            'country': forms.Select(attrs=({'placeholder': 'Country...'})),
            'company': forms.TextInput(attrs=({'placeholder': 'Company... (Optional)'})),

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
        self.fields['country'].queryset = Country.objects.filter(is_active=True)

    @classmethod
    def get_countries(cls):
        return list(Country.objects.filter(is_active=True))

    @classmethod
    def get_states(cls):
        return list(State.objects.filter(is_active=True))
