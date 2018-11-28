from django import forms

from .models import Ripoff, Product


class RipoffForm(forms.ModelForm):
    product_name = forms.CharField()

    class Meta:
        model = Ripoff

        fields = [
            'base_price',
            'location',
            'payment_type',
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['base_price'] > 99.99:
            raise forms.ValidationError("Base price must be less than 100 dollars!")

        return cleaned_data
