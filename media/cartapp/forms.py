from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Checkout

class MyPaymentForm(forms.ModelForm):
    card_number = forms.IntegerField(
        label='Card Number',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(9999999999999999)],
        widget=forms.TextInput(attrs={'type': 'tel', 'pattern': '\\d*'})
    )
    expiration_date = forms.DateField(
        label='Expiration Date (mm/dd/yyyy)',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'mm/dd/yyyy'})
    )
    cvv = forms.IntegerField(label='CVV', max_value=999999, required=True)

    class Meta:
        model = Checkout
        fields = ['shipping_address', 'payment_method', 'card_number', 'expiration_date', 'cvv']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Shipping Address'}),
            'payment_method': forms.Select(choices=[
                ('credit_card', 'Credit Card'),
                ('visa', 'Visa'),
                ('debit_card','Debit card')
                
            ]),
        }

    def __init__(self, *args, **kwargs):
        super(MyPaymentForm, self).__init__(*args, **kwargs)
        self.fields['shipping_address'].label = False  