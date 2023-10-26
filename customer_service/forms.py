from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone_number', 'address_uk', 'delivery_address', 'bed_type', 'requested_delivery_date']
