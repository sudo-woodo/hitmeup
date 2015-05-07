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
        'name': 'Email'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class PasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Current Password',
        'id': 'current_password',
        'name': 'Current Password'
    }))

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter New Password',
        'id': 'new_password',
        'name': 'New Password'
    }))


class EmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email',
        'id': 'email',
        'name': 'Email'
    }))


class EditForm(forms.ModelForm, PasswordForm, EmailForm):
    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'email')