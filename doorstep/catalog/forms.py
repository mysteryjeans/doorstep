from django import forms

from doorstep.catalog.models import Manufacturer, Category


class AdvancedSearchForm(forms.Form):
    """
    Advanced Catalog Search form
    """
    keyword = forms.CharField(max_length=15, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Search store...'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.filter(
        is_active=True), empty_label='all...')
    manufacturer = forms.ModelChoiceField(
        required=False, queryset=Manufacturer.objects.filter(is_active=True), empty_label='all...')
    price_from = forms.IntegerField(
        required=False, label='Price From', widget=forms.TextInput(attrs={'placeholder': 'From...'}))
    price_to = forms.IntegerField(
        required=False, label='Price To', widget=forms.TextInput(attrs={'placeholder': 'To...'}))

    def clean_price_to(self):
        price_from = self.cleaned_data.get('price_from', None)
        price_to = self.cleaned_data.get('price_to', None)

        if price_from and price_to and int(price_from) > int(price_to):
            raise forms.ValidationError("Please provide a valid price range.")

        return price_to
