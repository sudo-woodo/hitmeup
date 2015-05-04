from django.contrib.auth.models import User
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username',
        'id': 'user',
        'name': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
        'id': 'password',
        'name': 'Password'
    }))


class SignupForm(forms.ModelForm, UserForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'id': 'email',
        'name': 'email'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

class EditForm(forms.ModelForm, UserForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'id': 'email',
        'name': 'email'
    }))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')