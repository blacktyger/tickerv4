from django import forms
from django.forms import TextInput

from .models import Travel


class TravelForm(forms.ModelForm):
    # str(x).split('.')[2] for x in Job._meta.get_fields()
    class Meta:
        model = Travel
        fields = ['origin', 'destination', 'price', 'amount']
        widgets = {
            'origin': TextInput(attrs={
                'class': 'input',
                'placeholder': 'Address',
                'class': 'form-control',
                }),
            'destination': TextInput(attrs={
                'class': 'input',
                'placeholder': 'Address',
                'class': 'form-control',
                }),
            'price': TextInput(attrs={
                'class': 'input',
                'placeholder': 'Fuel Price',
                'class': 'form-control',
                }),
            'amount': TextInput(attrs={
                'class': 'input',
                'placeholder':
                    'Fuel Consumption',
                'class': 'form-control',
                })
            }
