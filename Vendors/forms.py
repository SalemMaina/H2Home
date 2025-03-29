from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'opening_time', 'closing_time', 'location',
            'website', 'description', 'price_per_litre', 'email', 'phone_number', 'image'
        ]
