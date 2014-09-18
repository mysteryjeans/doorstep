from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


# USER_AUTH_MODEL defined in settings.py
User = get_user_model()


class RegisterForm(forms.ModelForm):

    """
    Customer registration form
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your new password...'}),
                               min_length=8, max_length=50,
                               serror_messages={'required': 'Please enter your new password.'})
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your new password again...'}),
        max_length=50, error_messages={'required': 'Please re-enter your new password for confirmation.'})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender')
        widgets = {
            'username': forms.TextInput(attrs=({'placeholder': 'Choose a new username...'})),
            'email': forms.TextInput(attrs=({'placeholder': 'Email address...'})),
            'first_name': forms.TextInput(attrs=({'placeholder': 'First name...'})),
            'last_name': forms.TextInput(attrs=({'placeholder': 'Last name...'})),
            'gender': forms.RadioSelect(choices=User.GENDERS)
        }
        error_messages = {
            'username': {'required': 'Please choose a username.'},
            'gender': {'required': 'Please specify your gender.'}
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            raise ValidationError('Please enter you email address.')

        if User.objects.filter(email__iexact=email).count() > 0:
            raise ValidationError('User with this email address already exists.')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not first_name:
            raise ValidationError('Please enter your first name.')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not last_name:
            raise ValidationError('Please enter your last name.')

        return last_name

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if 'password' in self.cleaned_data and self.cleaned_data['password'] != confirm_password:
            raise forms.ValidationError("Your new password and confirm password didn't matched.")
        return confirm_password
