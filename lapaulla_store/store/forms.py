# store/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal

class LoginForm(AuthenticationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount to Deposit (₦)',
        min_value=Decimal('1.00'),
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )