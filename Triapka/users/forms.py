from django.contrib.auth.forms import AuthenticationForm , UserCreationForm ,UserChangeForm
from users.models import User
from django import forms

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username' ,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password' ,
    }))
    class Meta:
        model = User 
        fields = ('username' , 'password')

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username' ,
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First_name' ,
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last_name' ,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'email' ,
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password' ,
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password' ,
    }))
    class Meta:
        model = User 
        fields = ('username','first_name' , 'last_name', 'email' , 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = User 
        fields = ('username','first_name' , 'last_name', 'email' )
