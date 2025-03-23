from django import forms
from orders.models import Order

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Poland, Warszawa, ul. Mickiewicza,  d. 6'
    }))
   
    postal_code = forms.RegexField(regex=r'^\d{2}-?\d{3}$', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': '12-345'}), max_length=6)
    locality = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your City'}))
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Region'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'locality', 'region', 'phone_number',)
