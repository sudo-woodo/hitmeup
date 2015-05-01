from django.contrib.auth.models import User
from django import forms


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username',
        'id': 'signup_user',
        'name': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
        'id': 'signup_password',
        'name': 'Password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')
