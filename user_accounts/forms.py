from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator


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


class SignUpExtendedForm(forms.Form):

    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be between 10-15 digits")

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your First Name',
        'id': 'firstname',
        'name': 'firstname'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Last Name',
        'id': 'lastname',
        'name': 'lastname'
    }))

    phone = forms.CharField(
        required=False,
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Phone Number',
                'id': 'phone',
                'name': 'phone'
            }
        )
    )

    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write about a quick bio about yourself :^)',
                'id': 'bio',
                'name': 'bio'
            }
        )
    )